from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault('UPLOAD_ASSISTANT_DB', str(ROOT / 'data' / 'smoke_test.db'))

from backend.app import main


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main_smoke() -> None:
    if main.DB_PATH.exists():
        main.DB_PATH.unlink()
    main.init_db()
    previous_settings = {item.key: item.value for item in main.list_settings()}
    main.save_settings([main.AppSetting(key='enable_external_collection', value='false')])
    main.save_settings([
        main.AppSetting(key='temu_shop_account', value='My Smoke Shop'),
        main.AppSetting(key='temu_site', value='美国'),
        main.AppSetting(key='temu_product_template', value='My Product Template'),
        main.AppSetting(key='temu_size_template', value='My Size Template'),
        main.AppSetting(key='temu_warehouse_template', value='My Warehouse'),
        main.AppSetting(key='temu_logistics_template', value='My Logistics'),
    ])
    command = main.upload_rpa_command(r'D:\tmp\smoke.xlsx')
    assert_true('--shop-account' in command and command[command.index('--shop-account') + 1] == 'My Smoke Shop', 'shop account not passed to RPA')
    assert_true('--site' in command and command[command.index('--site') + 1] == '美国', 'site not passed to RPA')
    assert_true('--product-template' in command and command[command.index('--product-template') + 1] == 'My Product Template', 'product template not passed to RPA')
    assert_true('--size-template' in command and command[command.index('--size-template') + 1] == 'My Size Template', 'size template not passed to RPA')
    assert_true('--warehouse-template' in command and command[command.index('--warehouse-template') + 1] == 'My Warehouse', 'warehouse template not passed to RPA')
    assert_true('--logistics-template' in command and command[command.index('--logistics-template') + 1] == 'My Logistics', 'logistics template not passed to RPA')

    dashboard = main.dashboard()
    assert_true('product_count' in dashboard, 'dashboard missing product_count')
    status = main.system_status()
    assert_true(status['database_exists'], 'system status database check failed')
    assert_true('collection_preflight' in status, 'system status missing collection preflight')
    upload_preflight = main.upload_preflight()
    assert_true('items' in upload_preflight, 'upload preflight missing item diagnostics')
    assert_true('blocked_count' in upload_preflight['items'], 'upload preflight missing blocked count')
    settings = {item.key: item.value for item in main.list_settings()}
    assert_true('onebound_key' in settings and 'onebound_secret' in settings, 'onebound settings missing')
    rows = main.normalize_onebound_items(
        [{'title': 'Onebound Smoke Candidate', 'num_iid': '123456', 'price': '12.5', 'sales': '88', 'pic_url': 'https://img.example/a.jpg'}],
        '1688',
    )
    assert_true(rows[0]['url'].endswith('/123456.html'), 'onebound item url normalization failed')

    try:
        main.create_collection_task(
            main.CollectionTaskPayload(
                keyword='smoke test shorts',
                source='1688',
                mode='simulate',
                collector='local',
                target_count=2,
                min_price=10,
                max_price=30,
                blacklist='',
            )
        )
    except HTTPException as exc:
        assert_true(exc.status_code == 410, 'simulate collection was not removed')
    else:
        raise AssertionError('simulate collection unexpectedly succeeded')

    candidate = main.create_collection_item(
        main.CollectionItemPayload(
            title='Smoke Test Shorts Imported Candidate',
            source='外部文件',
            source_url='https://example.com/smoke-candidate',
            image_url='https://img.example.com/smoke.jpg',
            price=26.8,
            sales=500,
            image_count=12,
        )
    )
    candidates = [candidate]

    imported_products = main.import_collection_items(main.ImportCollectionPayload(ids=[candidates[0].id]))
    assert_true(len(imported_products) == 1, 'candidate import did not create product')
    detail_payload = {
        'item': {
            'title': 'Smoke Detail Denim Shorts',
            'price': '19.8',
            'props_name': '0:0:颜色:Blue;0:1:颜色:Black;1:0:尺码:S;1:1:尺码:M',
            'prop_imgs': {'prop_img': [{'properties': '0:0', 'url': 'https://img.example.com/blue-prop.jpg'}]},
            'item_imgs': [
                {'url': 'https://img.example.com/detail-main-1.jpg'},
                {'url': 'https://img.example.com/detail-main-2.jpg'},
            ],
            'skus': {'sku': [
                {'sku_id': 'sku-blue-s', 'properties': '0:0;1:0', 'properties_name': '0:0:颜色:Blue;1:0:尺码:S'},
                {'sku_id': 'sku-blue-m', 'properties': '0:0;1:1', 'properties_name': '0:0:颜色:Blue;1:1:尺码:M'},
            ]},
        }
    }
    with main.connect() as db:
        main.apply_detail_to_product(db, imported_products[0].id, 'https://detail.1688.com/offer/123456.html', detail_payload)
        db.commit()
    enriched_processing = main.get_processing_item(imported_products[0].id)
    assert_true(enriched_processing.detail_status == 'completed', 'detail snapshot status not exposed')
    assert_true('Blue' in enriched_processing.color and 'S' in enriched_processing.size, 'detail color/size did not map to processing item')
    assert_true(any(option.kind == 'detail_sku_image' for option in enriched_processing.image_options), 'detail sku images not available for image processing')
    delete_imported_candidate = main.delete_collection_items(main.CollectionBulkPayload(ids=[candidates[0].id]))
    assert_true(delete_imported_candidate['deleted_count'] == 1, 'imported collection item was not deleted')
    imported_product_still_exists = main.connect().execute('SELECT id FROM products WHERE id = ?', (imported_products[0].id,)).fetchone()
    assert_true(imported_product_still_exists is not None, 'deleting collection item removed product unexpectedly')

    try:
        main.generate_missing_image_placeholders()
    except HTTPException as exc:
        assert_true(exc.status_code == 410, 'placeholder generation was not removed')
    else:
        raise AssertionError('placeholder generation unexpectedly succeeded')

    with main.connect() as db:
        db.execute('DELETE FROM products WHERE id != ?', (imported_products[0].id,))
        db.commit()
    product = main.product_from_row(main.connect().execute('SELECT * FROM products WHERE id = ?', (imported_products[0].id,)).fetchone())
    processing_before_image = main.get_processing_item(product.id)
    assert_true(processing_before_image.image_options, 'processing item missing selectable image options')
    local_source_image = next((option.url for option in processing_before_image.image_options if option.url.startswith('/images/')), '')
    if local_source_image:
        try:
            main.process_product_image(main.ProcessImagePayload(product_id=product.id, source_image=local_source_image))
        except HTTPException as exc:
            assert_true(exc.status_code == 400 and '公网图片 URL' in str(exc.detail), 'local image source did not block clearly')
    selected_source_image = next((option.url for option in processing_before_image.image_options if option.url.startswith('http')), '')
    assert_true(selected_source_image, 'processing item missing public image option')
    try:
        main.process_product_image(main.ProcessImagePayload(product_id=product.id, source_image=selected_source_image))
    except HTTPException as exc:
        assert_true(exc.status_code == 400 and '图生图 API 未配置' in str(exc.detail), 'image processing did not block missing API key')
    else:
        tasks = main.list_product_image_tasks(product.id)
        assert_true(tasks and tasks[0].task_id, 'image processing did not create a provider task')
    generated = main.generate_processing_title(main.GenerateTitlePayload(product_id=product.id))
    assert_true(generated.english_title, 'title generation returned empty title')

    default_processing = main.get_processing_item(product.id).model_copy(
        update={
            'color': 'pending',
            'size': 'pending',
            'sku_code': f'{product.skc}-COLOR-SIZE',
        }
    )
    default_diagnostics = main.upload_item_diagnostics([default_processing])[0]
    assert_true(not default_diagnostics['ready'], 'default pending SKU item should not be upload-ready')
    assert_true('SKU Code 使用默认占位' in default_diagnostics['issues'], 'default SKU placeholder did not block upload')

    with main.connect() as db:
        db.execute(
            'UPDATE products SET main_image = ?, updated_at = ? WHERE id = ?',
            ('https://img.example.com/smoke-main.jpg', main.now_text(), product.id),
        )
        db.commit()

    processing = main.update_processing_item(
        product.id,
        main.ProcessingItemPayload(
            english_title='Smoke Test Product for Temu',
            color='Blue',
            size='S-XL',
            sku_code=f'{product.skc}-BLUE-SXL',
            declared_price=29.99,
            weight_g=420,
            length_cm=20,
            width_cm=15,
            height_cm=4,
            source_url='https://example.com/smoke',
            stock=888,
            ship_days=7,
        ),
    )
    assert_true(processing.english_title == 'Smoke Test Product for Temu', 'processing override did not persist')
    main.save_manual_color_image_assignment(main.ManualColorImageAssignmentPayload(product_id=product.id, color='Blue', slot_index=0, image_url='https://img.example.com/blue-a.jpg'))
    main.save_manual_color_image_assignment(main.ManualColorImageAssignmentPayload(product_id=product.id, color='Blue', slot_index=1, image_url='https://img.example.com/blue-b.jpg'))
    main.save_manual_color_image_assignment(main.ManualColorImageAssignmentPayload(product_id=product.id, color='Blue', slot_index=2, image_url='https://img.example.com/blue-c.jpg'))
    main.save_manual_color_image_assignment(main.ManualColorImageAssignmentPayload(product_id=product.id, color='Black', slot_index=0, image_url='https://img.example.com/black-a.jpg'))
    main.save_manual_color_image_assignment(main.ManualColorImageAssignmentPayload(product_id=product.id, color='Black', slot_index=1, image_url='https://img.example.com/black-b.jpg'))
    main.save_manual_color_image_assignment(main.ManualColorImageAssignmentPayload(product_id=product.id, color='Black', slot_index=2, image_url='https://img.example.com/black-c.jpg'))
    processing = main.get_processing_item(product.id)
    upload_rows = main.miaoshou_rows([processing])
    color_values = {row[5] for row in upload_rows}
    sku_codes = [row[10] for row in upload_rows]
    assert_true({'Blue', 'Black'}.issubset(color_values), 'miaoshou rows did not expand all colors')
    assert_true(len(sku_codes) == len(set(sku_codes)), 'miaoshou SKU codes are duplicated')

    export = main.export_miaoshou()
    assert_true(Path(export['path']).exists(), 'export file does not exist')

    upload_task = main.create_upload_task()
    assert_true(upload_task.total_count >= 1, 'upload task has no items')
    assert_true(upload_task.failed_count == 0, f'upload task has failed items: {upload_task.failed_count}')

    real_task = main.run_upload_task()
    assert_true(real_task.status == 'blocked', 'formal upload should be blocked by default safety switch')
    assert_true('enable_real_rpa is false' in real_task.run_log, 'formal upload did not record safety block reason')

    status_result = main.update_products_status(main.ProductBulkStatusPayload(ids=[product.id], status='待处理'))
    assert_true(status_result['updated_count'] == 1, 'bulk product status update failed')

    temp_task = main.create_upload_task()
    delete_result = main.delete_upload_task(temp_task.id)
    assert_true(delete_result['ok'], 'delete upload task failed')

    json_path = Path('data/smoke_external_result.json')
    json_path.write_text(
        json.dumps([
            {
                'title': 'Smoke External JSON Candidate',
                'url': 'https://example.com/smoke-json-candidate',
                'price': 18.8,
                'sales': 999,
                'image_count': 8,
            }
        ], ensure_ascii=False),
        encoding='utf-8',
    )
    rows = main.parse_collection_rows(json_path)
    inserted, skipped = main.insert_collection_rows(rows, 'SmokeJSON')
    assert_true(inserted + skipped >= 1, 'json import path did not process rows')

    main.save_settings(
        [
            main.AppSetting(key='enable_external_collection', value=previous_settings.get('enable_external_collection', 'false')),
            main.AppSetting(key='collection_mode', value=previous_settings.get('collection_mode', '1688')),
        ]
    )

    print('SMOKE_OK')


if __name__ == '__main__':
    main_smoke()




