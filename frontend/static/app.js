const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const backToTopButton = document.querySelector('#backToTopButton');
const productsBody = document.querySelector('#productsBody');
const dashboardCards = document.querySelector('#dashboardCards');
const selectAllProducts = document.querySelector('#selectAllProducts');
const bulkProductStatus = document.querySelector('#bulkProductStatus');
const bulkProductStatusButton = document.querySelector('#bulkProductStatusButton');
const bulkProductDeleteButton = document.querySelector('#bulkProductDeleteButton');
const searchInput = document.querySelector('#searchInput');
const productStatusFilter = document.querySelector('#productStatusFilter');
const productImageFilter = document.querySelector('#productImageFilter');
const searchButton = document.querySelector('#searchButton');
const refreshButton = document.querySelector('#refreshButton');
const batchImageInput = document.querySelector('#batchImageInput');
const newProductButton = document.querySelector('#newProductButton');
const modal = document.querySelector('#modal');
const productForm = document.querySelector('#productForm');
const closeModal = document.querySelector('#closeModal');
const cancelButton = document.querySelector('#cancelButton');
const formTitle = document.querySelector('#formTitle');
const collectionBody = document.querySelector('#collectionBody');
const selectAllCollection = document.querySelector('#selectAllCollection');
const importSelectedButton = document.querySelector('#importSelectedButton');
const deleteSelectedCollectionButton = document.querySelector('#deleteSelectedCollectionButton');
const applyCollectionFiltersButton = document.querySelector('#applyCollectionFiltersButton');
const collectionFileInput = document.querySelector('#collectionFileInput');
const collectionFileSource = document.querySelector('#collectionFileSource');
const startCollectionTaskButton = document.querySelector('#startCollectionTaskButton');
const collectionProgressBody = document.querySelector('#collectionProgressBody');
const collectionTasksBody = document.querySelector('#collectionTasksBody');
const clearCollectionTasksButton = document.querySelector('#clearCollectionTasksButton');
const collectionRequestModal = document.querySelector('#collectionRequestModal');
const collectionRequestContent = document.querySelector('#collectionRequestContent');
const closeCollectionRequestModal = document.querySelector('#closeCollectionRequestModal');
const imagePreviewModal = document.querySelector('#imagePreviewModal');
const imagePreviewImg = document.querySelector('#imagePreviewImg');
const imagePreviewTitle = document.querySelector('#imagePreviewTitle');
const imagePreviewLink = document.querySelector('#imagePreviewLink');
const hoverImagePreview = document.querySelector('#hoverImagePreview');
const hoverImagePreviewImg = hoverImagePreview?.querySelector('img');
const closeImagePreviewModal = document.querySelector('#closeImagePreviewModal');
const slotImagePickerModal = document.querySelector('#slotImagePickerModal');
const closeSlotImagePickerModal = document.querySelector('#closeSlotImagePickerModal');
const cancelSlotImagePickerButton = document.querySelector('#cancelSlotImagePickerButton');
const confirmSlotImagePickerButton = document.querySelector('#confirmSlotImagePickerButton');
const slotImagePickerTitle = document.querySelector('#slotImagePickerTitle');
const slotImagePickerHint = document.querySelector('#slotImagePickerHint');
const slotImagePickerCount = document.querySelector('#slotImagePickerCount');
const slotImagePickerGrid = document.querySelector('#slotImagePickerGrid');
const collectionResultFileInput = document.querySelector('#collectionResultFileInput');
let pendingCollectionResultTaskId = null;
let pendingSlotImagePick = null;
let pendingSlotImageUrls = new Set();
const processingBody = document.querySelector('#processingBody');
const processingDetailPanel = document.querySelector('#processingDetailPanel');
const processingDetailStatus = document.querySelector('#processingDetailStatus');
const processingStatusFilter = document.querySelector('#processingStatusFilter');
const selectAllProcessing = document.querySelector('#selectAllProcessing');
const processingBatchAction = document.querySelector('#processingBatchAction');
const runProcessingBatchActionButton = document.querySelector('#runProcessingBatchActionButton');
const processingSourceLabel = document.querySelector('#processingSourceLabel');
const refreshProcessingButton = document.querySelector('#refreshProcessingButton');
const exportMiaoshouButton = document.querySelector('#exportMiaoshouButton');
const processingModal = document.querySelector('#processingModal');
const processingForm = document.querySelector('#processingForm');
const closeProcessingModal = document.querySelector('#closeProcessingModal');
const cancelProcessingButton = document.querySelector('#cancelProcessingButton');
const createUploadTaskButton = document.querySelector('#createUploadTaskButton');
const createUploadTaskInlineButton = document.querySelector('#createUploadTaskInlineButton');
const saveUploadOperationSettingsButton = document.querySelector('#saveUploadOperationSettingsButton');
const clearUploadTasksButton = document.querySelector('#clearUploadTasksButton');
const preflightButton = document.querySelector('#preflightButton');
const preflightInlineButton = document.querySelector('#preflightInlineButton');
const realUploadButton = document.querySelector('#realUploadButton');
const realUploadInlineButton = document.querySelector('#realUploadInlineButton');
const preflightBox = document.querySelector('#preflightBox');
const uploadTasksBody = document.querySelector('#uploadTasksBody');
const publishRecordsBody = document.querySelector('#publishRecordsBody');
const missingImagesBox = document.querySelector('#missingImagesBox');
const logModal = document.querySelector('#logModal');
const logContent = document.querySelector('#logContent');
const closeLogModal = document.querySelector('#closeLogModal');
const appDialogModal = document.querySelector('#appDialogModal');
const appDialogTitle = document.querySelector('#appDialogTitle');
const appDialogMessage = document.querySelector('#appDialogMessage');
const appDialogOk = document.querySelector('#appDialogOk');
const appDialogCancel = document.querySelector('#appDialogCancel');
const appDialogClose = document.querySelector('#appDialogClose');
const operationLogBody = document.querySelector('#operationLogBody');
const operationProgressBar = document.querySelector('#operationProgressBar');
const operationStatusBadge = document.querySelector('#operationStatusBadge');
const clearOperationLogButton = document.querySelector('#clearOperationLogButton');
const temuRunStatusText = document.querySelector('#temuRunStatusText');
const refreshRecordsButton = document.querySelector('#refreshRecordsButton');
const retryFailedButton = document.querySelector('#retryFailedButton');
const recordsSearchInput = document.querySelector('#recordsSearchInput');
const recordsResultFilter = document.querySelector('#recordsResultFilter');
let products = [];
let collectionItems = [];
let collectionTasks = [];
let processingItems = [];
let selectedProcessingProductId = null;
let selectedProcessingIds = new Set();
let selectedProcessingImageUrls = new Map();
let processingFormMode = 'single';
let uploadTasks = [];
let publishRecords = [];
let missingImageProducts = [];
let operationLogs = [];
let operationProgress = 0;
let collectionProgressLogs = [];
let lastCollectionTaskLogKey = '';

function showAppDialog({ title = '提示', message = '', okText = '确定', cancelText = '取消', confirm = false } = {}) {
  if (!appDialogModal) {
    return Promise.resolve(window.alert(message));
  }
  appDialogTitle.textContent = title;
  appDialogMessage.textContent = message;
  appDialogOk.textContent = okText;
  appDialogCancel.textContent = cancelText;
  appDialogCancel.style.display = confirm ? '' : 'none';
  appDialogModal.classList.remove('hidden');
  return new Promise(resolve => {
    const cleanup = value => {
      appDialogModal.classList.add('hidden');
      appDialogOk.onclick = null;
      appDialogCancel.onclick = null;
      appDialogClose.onclick = null;
      resolve(value);
    };
    appDialogOk.onclick = () => cleanup(true);
    appDialogCancel.onclick = () => cleanup(false);
    appDialogClose.onclick = () => cleanup(false);
  });
}

function notify(message, title = '提示') {
  addOperationLog(title, 'info', message, operationProgress || 8);
  return showAppDialog({ title, message, okText: '知道了' });
}

function askConfirm(message, title = '确认操作') {
  return showAppDialog({ title, message, okText: '确认', cancelText: '取消', confirm: true });
}

function renderOperationLogs() {
  if (!operationLogBody) return;
  if (operationStatusBadge) {
    operationStatusBadge.textContent = operationLogs[0]?.statusText || '待开始';
    operationStatusBadge.className = `badge ${operationLogs[0]?.badge || 'blue'}`;
  }
  if (temuRunStatusText) temuRunStatusText.textContent = operationLogs[0]?.statusText || '就绪';
  if (operationProgressBar) operationProgressBar.style.width = `${Math.max(0, Math.min(100, operationProgress))}%`;
  if (!operationLogs.length) {
    operationLogBody.textContent = '[Temu] 模块已加载';
    return;
  }
  operationLogBody.textContent = operationLogs.slice(0, 50).map(log => `[${log.time}] ${log.step} · ${log.statusText}\n${log.message}`).join('\n\n');
}

function addOperationLog(step, type = 'info', message = '', progress = operationProgress) {
  const statusMap = {
    running: ['处理中', 'blue'],
    success: ['完成', 'green'],
    error: ['需处理', 'orange'],
    info: ['记录', 'blue'],
  };
  const [statusText, badge] = statusMap[type] || statusMap.info;
  operationProgress = progress;
  operationLogs.unshift({ time: new Date().toLocaleTimeString(), step, type, statusText, badge, message });
  renderOperationLogs();
}

function renderCollectionProgressLogs() {
  if (!collectionProgressBody) return;
  if (!collectionProgressLogs.length) {
    collectionProgressBody.innerHTML = '<div class="chat-empty">暂无采集日志</div>';
    return;
  }
  collectionProgressBody.innerHTML = collectionProgressLogs.slice(0, 50).map(log => `
    <div class="chat-row ${log.type}">
      <div class="chat-avatar">${log.type === 'success' ? '✓' : (log.type === 'error' ? '!' : '…')}</div>
      <div class="chat-bubble">
        <div class="chat-meta"><b>${log.step}</b><span>${log.time}</span><em class="log-status ${log.type}">${log.statusText}</em></div>
        <div class="chat-message">${log.message}</div>
      </div>
    </div>
  `).join('');
}

function addCollectionProgressLog(step, type = 'info', message = '') {
  const statusMap = { running: '处理中', success: '完成', error: '需处理', info: '记录' };
  collectionProgressLogs.unshift({ time: new Date().toLocaleTimeString(), step, type, statusText: statusMap[type] || statusMap.info, message });
  renderCollectionProgressLogs();
}

const saveApiButton = document.querySelector('#saveApiButton');
const saveSettingsButton = document.querySelector('#saveSettingsButton');
const refreshSystemStatusButton = document.querySelector('#refreshSystemStatusButton');
const systemStatusBox = document.querySelector('#systemStatusBox');
const cleanupTestDataButton = document.querySelector('#cleanupTestDataButton');
const promptsBody = document.querySelector('#promptsBody');
const newPromptButton = document.querySelector('#newPromptButton');
const promptModal = document.querySelector('#promptModal');
const promptForm = document.querySelector('#promptForm');
const closePromptModal = document.querySelector('#closePromptModal');
const cancelPromptButton = document.querySelector('#cancelPromptButton');
let apiConfigs = [];
let appSettings = [];
let prompts = [];

function renderDashboard(stats) {
  if (!dashboardCards) return;
  const cards = [
    ['商品总数', stats.product_count, 'blue'],
    ['可上货商品', stats.ready_products, 'green'],
    ['待补主图', stats.missing_images, stats.missing_images ? 'orange' : 'green'],
    ['任务总数', stats.task_count, 'purple'],
  ];
  dashboardCards.innerHTML = cards.map(([label, value, color]) => `
    <div class="metric-card">
      <div class="metric-label">${label}</div>
      <div class="metric-value"><span class="badge ${color}">${value}</span></div>
    </div>
  `).join('');
}

async function loadDashboard() {
  if (!dashboardCards) return;
  renderDashboard(await fetchJson('/api/dashboard'));
}

function byId(id) { return document.querySelector(`#${id}`); }
function settingValue(key) { return appSettings.find(item => item.key === key)?.value || ''; }
function apiConfig(key) { return apiConfigs.find(item => item.key === key) || {}; }

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    let message = '请求失败';
    try {
      const error = await response.json();
      message = error.detail || message;
    } catch (_) {
      message = response.statusText || message;
    }
    throw new Error(message);
  }
  return response.json();
}

function fillApiForm() {
  const deepseek = apiConfig('deepseek');
  const image = apiConfig('image');
  const vision = apiConfig('vision');
  if (!byId('deepseekName')) return;
  byId('deepseekName').value = deepseek.name || '';
  byId('deepseekEnabled').value = String(deepseek.enabled ?? true);
  byId('deepseekBaseUrl').value = deepseek.base_url || '';
  byId('deepseekModel').value = deepseek.model || '';
  byId('deepseekApiKey').value = deepseek.api_key || '';
  byId('deepseekUsage').value = deepseek.usage || '';
  byId('imageName').value = image.name || '';
  byId('imageEnabled').value = String(image.enabled ?? true);
  byId('imageBaseUrl').value = image.base_url || '';
  byId('imageModel').value = image.model || '';
  byId('imageApiKey').value = image.api_key || '';
  byId('imageUsage').value = image.usage || '';
  if (byId('visionName')) {
    byId('visionName').value = vision.name || '豆包视觉识别';
    byId('visionEnabled').value = String(vision.enabled ?? true);
    byId('visionBaseUrl').value = vision.base_url || 'https://ark.cn-beijing.volces.com/api/v3';
    byId('visionModel').value = vision.model || 'doubao-1.5-vision-pro-32k';
    byId('visionApiKey').value = vision.api_key || '';
    byId('visionUsage').value = vision.usage || 'SKC颜色图片识别';
  }
}

function fillSettingsForm() {
  if (byId('settingRunMode')) byId('settingRunMode').value = settingValue('run_mode') || 'headless';
  if (byId('settingMaxRetries')) byId('settingMaxRetries').value = settingValue('max_retries') || '2';

  if (byId('settingUploadImageSource')) byId('settingUploadImageSource').value = settingValue('upload_image_source') || '';
  if (byId('settingCosRegion')) byId('settingCosRegion').value = settingValue('cos_region') || '';
  if (byId('settingCosBucket')) byId('settingCosBucket').value = settingValue('cos_bucket') || '';
  if (byId('settingCosPrefix')) byId('settingCosPrefix').value = settingValue('cos_prefix') || '';
  if (byId('settingEnableRealRpa')) byId('settingEnableRealRpa').value = settingValue('enable_real_rpa') || 'false';
  if (byId('settingExecutorMode')) byId('settingExecutorMode').value = settingValue('executor_mode') || 'local_python';
  if (byId('settingExecutorServerUrl')) byId('settingExecutorServerUrl').value = settingValue('executor_server_url') || window.location.origin;
  if (byId('settingExecutorBindCode')) byId('settingExecutorBindCode').value = settingValue('executor_bind_code') || '';
  if (byId('settingExecutorDownloadUrl')) byId('settingExecutorDownloadUrl').value = settingValue('executor_download_url') || '';
  if (byId('settingExecutorVersion')) byId('settingExecutorVersion').value = settingValue('executor_version') || '0.1.0';
  if (byId('settingExecutorPollSeconds')) byId('settingExecutorPollSeconds').value = settingValue('executor_poll_seconds') || '5';
  if (byId('settingExecutorHeartbeatTimeout')) byId('settingExecutorHeartbeatTimeout').value = settingValue('executor_heartbeat_timeout') || '60';
  if (byId('settingExecutorTaskScope')) byId('settingExecutorTaskScope').value = settingValue('executor_task_scope') || 'manual';
  if (byId('settingUploadFillSkc')) byId('settingUploadFillSkc').value = settingValue('upload_fill_skc') || 'true';
  if (byId('settingUploadSkcMissingPolicy')) byId('settingUploadSkcMissingPolicy').value = settingValue('upload_skc_missing_policy') || 'pause';
  if (byId('settingUploadAutoSubmit')) byId('settingUploadAutoSubmit').value = settingValue('upload_auto_submit') || 'false';
  if (byId('settingUploadErrorPolicy')) byId('settingUploadErrorPolicy').value = settingValue('upload_error_policy') || 'skip';
  if (byId('settingUploadSaveScreenshots')) byId('settingUploadSaveScreenshots').value = settingValue('upload_save_screenshots') || 'false';
  if (byId('settingUploadSaveHtml')) byId('settingUploadSaveHtml').value = settingValue('upload_save_html') || 'false';
  if (byId('settingUploadTrace')) byId('settingUploadTrace').value = settingValue('upload_trace') || 'off';
  if (byId('settingUploadStepDelayMs')) byId('settingUploadStepDelayMs').value = settingValue('upload_step_delay_ms') || '500';
  if (byId('settingTemuShopAccount')) byId('settingTemuShopAccount').value = settingValue('temu_shop_account') || '';
  if (byId('settingTemuSite')) byId('settingTemuSite').value = settingValue('temu_site') || '美国站';
  if (byId('settingTemuProductTemplate')) byId('settingTemuProductTemplate').value = settingValue('temu_product_template') || '';
  if (byId('settingTemuSizeCategory')) byId('settingTemuSizeCategory').value = settingValue('temu_size_category') || '';
  if (byId('settingTemuSizeTemplate')) byId('settingTemuSizeTemplate').value = settingValue('temu_size_template') || '';
  if (byId('settingTemuWarehouseTemplate')) byId('settingTemuWarehouseTemplate').value = settingValue('temu_warehouse_template') || '';
  if (byId('settingTemuLogisticsTemplate')) byId('settingTemuLogisticsTemplate').value = settingValue('temu_logistics_template') || '';
  if (byId('settingTemuShipDays')) byId('settingTemuShipDays').value = settingValue('temu_ship_days') || '9';
  if (byId('settingTemuDeclareMarkup')) byId('settingTemuDeclareMarkup').value = settingValue('temu_declare_markup') || '239.0';
  if (byId('settingTemuDefaultWeightG')) byId('settingTemuDefaultWeightG').value = settingValue('temu_default_weight_g') || '350';
  if (byId('settingTemuDefaultStock')) byId('settingTemuDefaultStock').value = settingValue('temu_default_stock') || '999';
  if (byId('settingTemuPackageLengthCm')) byId('settingTemuPackageLengthCm').value = settingValue('temu_package_length_cm') || '10';
  if (byId('settingTemuPackageWidthCm')) byId('settingTemuPackageWidthCm').value = settingValue('temu_package_width_cm') || '5';
  if (byId('settingTemuPackageHeightCm')) byId('settingTemuPackageHeightCm').value = settingValue('temu_package_height_cm') || '1';
  if (byId('settingTemu1688ExcelPath')) byId('settingTemu1688ExcelPath').value = settingValue('temu_1688_excel_path') || '';
  if (byId('settingTemuBatchLimit')) byId('settingTemuBatchLimit').value = settingValue('temu_batch_limit') || '';
  if (byId('settingTemuStartSkc')) byId('settingTemuStartSkc').value = settingValue('temu_start_skc') || '';
  if (byId('settingTemuAppendSkuSuffix')) byId('settingTemuAppendSkuSuffix').checked = settingValue('temu_append_sku_suffix') === 'true';
  if (byId('settingTemuAddModelInfo')) byId('settingTemuAddModelInfo').checked = settingValue('temu_add_model_info') === 'true';
  if (byId('settingTemuModelIndex')) byId('settingTemuModelIndex').value = settingValue('temu_model_index') || '2';
  if (byId('settingCollectionMode')) byId('settingCollectionMode').value = settingValue('collection_mode') || '1688';
  if (byId('settingEnableExternalCollection')) byId('settingEnableExternalCollection').value = settingValue('enable_external_collection') || 'false';
  if (byId('settingOneboundKey')) byId('settingOneboundKey').value = settingValue('onebound_key');
  if (byId('settingOneboundSecret')) byId('settingOneboundSecret').value = settingValue('onebound_secret');
if (byId('setting1688Cookie')) byId('setting1688Cookie').value = settingValue('1688_cookie');
}

function renderPrompts() {
  if (!promptsBody) return;
  if (!prompts.length) {
    promptsBody.innerHTML = '<tr><td class="empty-row" colspan="6">暂无提示词模板</td></tr>';
    return;
  }
  promptsBody.innerHTML = prompts.map(prompt => `
    <tr>
      <td>${prompt.name}</td>
      <td>${prompt.category}</td>
      <td>${prompt.prompt_type}</td>
      <td>${prompt.usage}</td>
      <td><span class="badge ${prompt.status === '启用中' ? 'green' : 'orange'}">${prompt.status}</span></td>
      <td><button class="btn ghost" data-prompt-edit="${prompt.id}">编辑</button><button class="btn outline-orange" data-prompt-delete="${prompt.id}">删除</button></td>
    </tr>
  `).join('');
}

async function loadApiConfigs() {
  if (!saveApiButton) return;
  apiConfigs = await fetchJson('/api/config/apis');
  fillApiForm();
}

async function saveApiConfigs() {
  const payloads = [
    ['deepseek', { key: 'deepseek', name: byId('deepseekName').value, enabled: byId('deepseekEnabled').value === 'true', base_url: byId('deepseekBaseUrl').value, model: byId('deepseekModel').value, api_key: byId('deepseekApiKey').value, usage: byId('deepseekUsage').value }],
    ['image', { key: 'image', name: byId('imageName').value, enabled: byId('imageEnabled').value === 'true', base_url: byId('imageBaseUrl').value, model: byId('imageModel').value, api_key: byId('imageApiKey').value, usage: byId('imageUsage').value }],
  ];
  if (byId('visionName')) {
    payloads.push(['vision', { key: 'vision', name: byId('visionName').value, enabled: byId('visionEnabled').value === 'true', base_url: byId('visionBaseUrl').value, model: byId('visionModel').value, api_key: byId('visionApiKey').value, usage: byId('visionUsage').value }]);
  }
  for (const [key, payload] of payloads) {
    await fetch(`/api/config/apis/${key}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  }
  await saveSettings({ silent: true });
  await loadApiConfigs();
  await notify('API / COS / 采集配置已保存');
}

async function loadSettings() {
  if (!saveSettingsButton && !byId('settingCosRegion') && !byId('settingCollectionMode')) return;
  appSettings = await fetchJson('/api/settings');
  fillSettingsForm();
}

async function saveSettings(options = {}) {
  const silent = Boolean(options.silent);
  const payload = [
    { key: 'run_mode', value: byId('settingRunMode')?.value || 'headless' },
    { key: 'max_retries', value: byId('settingMaxRetries')?.value || '2' },
    { key: 'upload_image_source', value: byId('settingUploadImageSource')?.value || '' },
    { key: 'cos_region', value: byId('settingCosRegion')?.value || '' },
    { key: 'cos_bucket', value: byId('settingCosBucket')?.value || '' },
    { key: 'cos_prefix', value: byId('settingCosPrefix')?.value || '' },
    { key: 'enable_real_rpa', value: byId('settingEnableRealRpa')?.value || 'false' },
    { key: 'executor_mode', value: byId('settingExecutorMode')?.value || 'local_python' },
    { key: 'executor_server_url', value: byId('settingExecutorServerUrl')?.value || window.location.origin },
    { key: 'executor_bind_code', value: byId('settingExecutorBindCode')?.value || '' },
    { key: 'executor_download_url', value: byId('settingExecutorDownloadUrl')?.value || '' },
    { key: 'executor_version', value: byId('settingExecutorVersion')?.value || '0.1.0' },
    { key: 'executor_poll_seconds', value: byId('settingExecutorPollSeconds')?.value || '5' },
    { key: 'executor_heartbeat_timeout', value: byId('settingExecutorHeartbeatTimeout')?.value || '60' },
    { key: 'executor_task_scope', value: byId('settingExecutorTaskScope')?.value || 'manual' },
    { key: 'upload_fill_skc', value: byId('settingUploadFillSkc')?.value || 'true' },
    { key: 'upload_skc_missing_policy', value: byId('settingUploadSkcMissingPolicy')?.value || 'pause' },
    { key: 'upload_auto_submit', value: byId('settingUploadAutoSubmit')?.value || 'false' },
    { key: 'upload_error_policy', value: byId('settingUploadErrorPolicy')?.value || 'skip' },
    { key: 'upload_save_screenshots', value: byId('settingUploadSaveScreenshots')?.value || 'false' },
    { key: 'upload_save_html', value: byId('settingUploadSaveHtml')?.value || 'false' },
    { key: 'upload_trace', value: byId('settingUploadTrace')?.value || 'off' },
    { key: 'upload_step_delay_ms', value: byId('settingUploadStepDelayMs')?.value || '500' },
    { key: 'temu_shop_account', value: byId('settingTemuShopAccount')?.value || '' },
    { key: 'temu_site', value: byId('settingTemuSite')?.value || '美国站' },
    { key: 'temu_product_template', value: byId('settingTemuProductTemplate')?.value || '' },
    { key: 'temu_size_category', value: byId('settingTemuSizeCategory')?.value || '' },
    { key: 'temu_size_template', value: byId('settingTemuSizeTemplate')?.value || '' },
    { key: 'temu_warehouse_template', value: byId('settingTemuWarehouseTemplate')?.value || '' },
    { key: 'temu_logistics_template', value: byId('settingTemuLogisticsTemplate')?.value || '' },
    { key: 'temu_ship_days', value: byId('settingTemuShipDays')?.value || '9' },
    { key: 'temu_declare_markup', value: byId('settingTemuDeclareMarkup')?.value || '239.0' },
    { key: 'temu_default_weight_g', value: byId('settingTemuDefaultWeightG')?.value || '350' },
    { key: 'temu_default_stock', value: byId('settingTemuDefaultStock')?.value || '999' },
    { key: 'temu_package_length_cm', value: byId('settingTemuPackageLengthCm')?.value || '10' },
    { key: 'temu_package_width_cm', value: byId('settingTemuPackageWidthCm')?.value || '5' },
    { key: 'temu_package_height_cm', value: byId('settingTemuPackageHeightCm')?.value || '1' },
    { key: 'temu_1688_excel_path', value: byId('settingTemu1688ExcelPath')?.value || '' },
    { key: 'temu_batch_limit', value: byId('settingTemuBatchLimit')?.value || '' },
    { key: 'temu_start_skc', value: byId('settingTemuStartSkc')?.value || '' },
    { key: 'temu_append_sku_suffix', value: byId('settingTemuAppendSkuSuffix')?.checked ? 'true' : 'false' },
    { key: 'temu_add_model_info', value: byId('settingTemuAddModelInfo')?.checked ? 'true' : 'false' },
    { key: 'temu_model_index', value: byId('settingTemuModelIndex')?.value || '2' },
    { key: 'collection_mode', value: byId('settingCollectionMode')?.value || '1688' },
    { key: 'enable_external_collection', value: byId('settingEnableExternalCollection')?.value || 'false' },
    { key: 'onebound_key', value: byId('settingOneboundKey')?.value || '' },
    { key: 'onebound_secret', value: byId('settingOneboundSecret')?.value || '' },
    { key: '1688_cookie', value: byId('setting1688Cookie')?.value || '' },
];
  await fetch('/api/settings', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  await loadSettings();
  await loadSystemStatus();
  if (!silent) await notify('设置已保存');
}

async function loadSystemStatus() {
  if (!systemStatusBox) return;
  const status = await fetchJson('/api/system/status');
  const checklist = (status.checklist || []).map(item => `
    <tr>
      <td>${item.label}</td>
      <td><span class="badge ${item.ok ? 'green' : 'orange'}">${item.ok ? '可用' : '需处理'}</span></td>
      <td>${item.action}</td>
    </tr>
  `).join('');
  systemStatusBox.innerHTML = `
    <div style="text-align:left; line-height:1.9;">
      <div class="table-wrap" style="margin-bottom:16px;"><table style="min-width:720px;"><thead><tr><th>检查项</th><th>状态</th><th>建议</th></tr></thead><tbody>${checklist}</tbody></table></div>
      <div><b>数据库：</b>${status.database_exists ? '✅' : '⚠️'} ${status.database}</div>
      <div><b>图片目录：</b>${status.image_dir_exists ? '✅' : '⚠️'} ${status.image_dir}</div>
      <div><b>真实 RPA：</b><span class="badge ${status.enable_real_rpa === 'true' ? 'orange' : 'green'}">${status.enable_real_rpa === 'true' ? '已开启' : '安全关闭'}</span></div>
      <div><b>外部采集执行：</b><span class="badge ${status.enable_external_collection === 'true' ? 'orange' : 'green'}">${status.enable_external_collection === 'true' ? '已开启' : '安全关闭'}</span></div>
      <div><b>默认采集模式：</b>${status.collection_mode}</div>
      <div><b>店小秘脚本目录：</b>${status.script_dir_exists ? '✅' : '⚠️'} ${status.script_dir}</div>
      <div><b>本地执行器：</b>${status.executor?.mode || '-'} · v${status.executor?.version || '-'} · ${status.executor?.server_url || '-'}</div>
      <div><b>上货流程：</b>SKC ${status.upload_flow?.fill_skc === 'true' ? '自动填写' : '不填写'} · 自动提交 ${status.upload_flow?.auto_submit === 'true' ? '开启' : '关闭'} · Trace ${status.upload_flow?.trace || '-'}</div>
      <div><b>上货预检：</b><span class="badge ${status.upload_preflight.ready ? 'green' : 'orange'}">${status.upload_preflight.ready ? '通过' : '需处理'}</span></div>
      <div><b>1688 采集：</b>${readyBadge(status.collection_preflight['1688'].configured)} · ${status.collection_preflight['1688'].onebound_configured ? 'API 已配置' : (status.collection_preflight['1688'].inline_cookie_configured ? '已粘贴 Cookie' : status.collection_preflight['1688'].cookie_path)}</div>
    </div>
  `;
}

async function cleanupTestData() {
  if (!await askConfirm('确认清理 smoke/example.local/测试 这类测试数据吗？真实采集商品不会按这个规则删除。')) return;
  const result = await fetchJson('/api/dev/cleanup-test-data', { method: 'POST' });
  await notify(`已清理：商品 ${result.deleted_products}，候选 ${result.deleted_collection_items}，采集任务 ${result.deleted_collection_tasks}`);
  await refreshOperationalViews();
  await loadCollectionItems();
  await loadCollectionTasks();
  await loadProcessingItems();
  await loadSystemStatus();
}

async function loadPrompts() {
  if (!promptsBody) return;
  prompts = await fetchJson('/api/prompts');
  renderPrompts();
}

async function createPrompt() {
  openPromptForm();
}

function openPromptForm(promptItem = null) {
  byId('promptFormTitle').textContent = promptItem ? '编辑提示词' : '新增提示词';
  byId('promptId').value = promptItem?.id || '';
  byId('promptName').value = promptItem?.name || '';
  byId('promptCategory').value = promptItem?.category || '女装短裤';
  byId('promptType').value = promptItem?.prompt_type || '标题提示词';
  byId('promptUsage').value = promptItem?.usage || '标题生成';
  byId('promptStatus').value = promptItem?.status || '启用中';
  byId('promptContent').value = promptItem?.content || '';
  promptModal.classList.remove('hidden');
}

function closePromptForm() {
  promptModal?.classList.add('hidden');
  promptForm?.reset();
}

function promptPayload() {
  return {
    name: byId('promptName').value.trim(),
    category: byId('promptCategory').value.trim(),
    prompt_type: byId('promptType').value.trim(),
    usage: byId('promptUsage').value.trim(),
    content: byId('promptContent').value.trim(),
    status: byId('promptStatus').value,
  };
}

async function refreshTaskViews() {
  await loadUploadTasks();
  await loadPublishRecords();
  await loadMissingImages();
}
setInterval(refreshTaskViews, 10000);
promptsBody?.addEventListener('click', async event => {
  const editId = event.target.dataset.promptEdit;
  const deleteId = event.target.dataset.promptDelete;
  if (editId) {
    const current = prompts.find(item => item.id === Number(editId));
    openPromptForm(current);
  }
  if (deleteId && await askConfirm('确定删除这个提示词吗？')) {
    await fetch(`/api/prompts/${deleteId}`, { method: 'DELETE' });
    await loadPrompts();
  }
});


navItems.forEach(item => {
  item.addEventListener('click', () => {
    navItems.forEach(nav => nav.classList.remove('active'));
    pages.forEach(page => page.classList.remove('active-page'));
    item.classList.add('active');
    document.querySelector(`#${item.dataset.page}`)?.classList.add('active-page');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});

function updateBackToTopVisibility() {
  if (!backToTopButton) return;
  backToTopButton.classList.toggle('hidden', window.scrollY < 320);
}

backToTopButton?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
window.addEventListener('scroll', updateBackToTopVisibility, { passive: true });
updateBackToTopVisibility();

function money(value) {
  return `¥${Number(value || 0).toFixed(1)}`;
}

function statusClass(status) {
  if (status.includes('补') || status.includes('待') || status.includes('pending')) return 'orange';
  if (status.includes('失败') || status.includes('缺')) return 'red';
  return 'green';
}

function productStatusText(status) {
  const map = {
    pending_main_image: '待补主图',
    pending: '待处理',
  };
  return map[status] || status;
}

function collectionStatusText(status) {
  const map = {
    pending: '待确认',
    imported: '已加入商品库',
    skipped: '已跳过',
    running: '运行中',
    completed: '已完成',
    empty: '无结果',
    external_pending: '待人工确认',
    blocked: '已阻断',
  };
  return map[status] || status;
}

function collectionTaskStatusClass(status) {
  if (status === 'completed') return 'green';
  if (status === 'failed') return 'red';
  if (status === 'empty' || status === 'external_pending' || status === 'blocked') return 'orange';
  return 'blue';
}

function readyBadge(ok) {
  return `<span class="badge ${ok ? 'green' : 'orange'}">${ok ? '就绪' : '需配置'}</span>`;
}



function taskStatusText(status) {
  const map = {
    ready: '就绪',
    needs_review: '需处理',
    pending: '等待中',
    blocked: '已阻断',
    rpa_success: 'RPA 成功',
    rpa_failed: 'RPA 失败',
  };
  return map[status] || status;
}

function processingStatusText(status) {
  const map = {
    pending: '待处理',
    has_main_image: '已有主图',
    missing_main_image: '待补主图',
    ready_to_export: '可生成表格',
    needs_image: '待补主图',
  };
  return map[status] || status;
}

function isProcessingReady(status) {
  return status === 'has_main_image' || status === 'ready_to_export';
}

function processingStatusClass(status) {
  return isProcessingReady(status) ? 'green' : 'red';
}

function processingColorReadiness(item) {
  const imageOptions = item.image_options || [];
  const matrix = buildVariantMatrix(item, imageOptions);
  const assignmentsByColor = new Map();
  (item.color_image_assignments || []).forEach(assignment => {
    const color = cleanSpecLabel(assignment.color, 'color');
    const imageUrl = assignment.image_url || assignment.url || '';
    if (!color || !imageUrl) return;
    if (!assignmentsByColor.has(color)) assignmentsByColor.set(color, new Set());
    assignmentsByColor.get(color).add(imageUrl);
  });
  const colors = matrix.colors.map(entry => entry.color).filter(Boolean);
  const missingColors = colors.filter(color => (assignmentsByColor.get(color)?.size || 0) < 3);
  return {
    ready: Boolean(colors.length) && missingColors.length === 0,
    colors,
    missingColors,
  };
}

function processingCardClass(item) {
  return processingColorReadiness(item).ready ? 'sku-images-ok' : 'sku-images-missing';
}

function processingUploadBadge(item) {
  return processingColorReadiness(item).ready
    ? '<span class="badge green">可导出</span>'
    : '<span class="badge red">需补图</span>';
}

function isPublishSuccess(result) {
  return result === 'Success' || result === '成功';
}



function renderMissingImages() {
  if (!missingImagesBox) return;
  if (!missingImageProducts.length) {
    missingImagesBox.innerHTML = '<div><div class="badge green">主图齐全</div><div style="margin-top:8px;">当前商品都已有商品库主图，可继续生成任务。</div></div>';
    return;
  }
  missingImagesBox.innerHTML = `
    <div style="text-align:left; line-height:1.8; width:100%;">
      <div><span class="badge orange">待补主图：${missingImageProducts.length}</span></div>
      <div>${missingImageProducts.map(product => `${product.skc} · ${product.title}`).join('<br/>')}</div>
      <div style="margin-top:8px; color:#6b7280;">请补充商品实拍/供应商图后再上货。</div>
    </div>
  `;
}

async function loadMissingImages() {
  if (!missingImagesBox) return;
  missingImageProducts = await fetchJson('/api/products/missing-images');
  renderMissingImages();
}

async function openTaskLog(taskId) {
  const response = await fetch(`/api/upload-tasks/${taskId}/log`);
  const result = await response.json();
  const manifestResponse = await fetch(`/api/upload-tasks/${taskId}/manifest`);
  const manifest = await manifestResponse.json();
  logContent.textContent = `Log Path: ${result.path}\nManifest Path: ${manifest.path}\n\n${result.content || 'No log content.'}\n\nManifest:\n${JSON.stringify(manifest.content || {}, null, 2)}`;
  logModal.classList.remove('hidden');
}

function renderUploadTasks() {
  if (!uploadTasksBody) return;
  if (!uploadTasks.length) {
    uploadTasksBody.innerHTML = '<tr><td class="empty-row" colspan="9">暂无上货任务，点击“创建上货任务”生成</td></tr>';
    return;
  }
  uploadTasksBody.innerHTML = uploadTasks.map(task => `
    <tr>
      <td>${task.name}</td>
      <td><span class="badge ${task.status === 'ready' ? 'green' : 'orange'}">${taskStatusText(task.status)}</span></td>
      <td>${task.total_count}</td>
      <td>${task.success_count}</td>
      <td>${task.failed_count}</td>
      <td>${task.export_path ? `<a href="/api/export/miaoshou/${task.export_path.split('\\').pop().split('/').pop()}" target="_blank">下载表格</a>` : '-'}</td>
      <td>${task.run_log || '-'}</td>
      <td><button class="btn ghost" data-log-task="${task.id}">Log</button><button class="btn outline-orange" data-delete-task="${task.id}">删除</button></td>
      <td>${task.created_at}</td>
    </tr>
  `).join('');
}

function renderPublishRecords() {
  if (!publishRecordsBody) return;
  if (!publishRecords.length) {
    publishRecordsBody.innerHTML = '<tr><td class="empty-row" colspan="5">暂无发布记录，先创建上货任务</td></tr>';
    return;
  }
  publishRecordsBody.innerHTML = publishRecords.map(record => `
    <tr>
      <td><span class="badge ${isPublishSuccess(record.result) ? 'green' : 'red'}">${record.result}</span></td>
      <td>${record.skc}</td>
      <td>${record.title}</td>
      <td>${record.reason || '-'}</td>
      <td>${record.created_at}</td>
    </tr>
  `).join('');
}

async function loadUploadTasks() {
  if (!uploadTasksBody) return;
  uploadTasks = await fetchJson('/api/upload-tasks');
  renderUploadTasks();
}

async function loadPublishRecords() {
  if (!publishRecordsBody) return;
  const params = new URLSearchParams();
  if (recordsSearchInput?.value.trim()) params.set('q', recordsSearchInput.value.trim());
  if (recordsResultFilter?.value) params.set('result', recordsResultFilter.value);
  publishRecords = await fetchJson(`/api/publish-records${params.toString() ? `?${params}` : ''}`);
  renderPublishRecords();
}

async function exportMiaoshou() {
  addOperationLog('生成店小秘表', 'running', '正在导出 xlsx 并准备 RPA 图片目录', 18);
  const response = await fetch('/api/export/miaoshou', { method: 'POST' });
  const result = await response.json();
  addOperationLog('生成店小秘表', 'success', `已生成：${result.path}`, 38);
  await notify(`已生成：${result.path}`);
  if (result.download_url) window.open(result.download_url, '_blank');
}



async function runPreflight() {
  if (!preflightBox) return;
  addOperationLog('上货预检', 'running', '正在检查脚本、导出表、图片目录和商品字段', 10);
  const response = await fetch('/api/upload/preflight');
  const result = await response.json();
  const scriptRows = Object.entries(result.scripts).map(([name, ok]) => `${ok ? 'OK' : '缺失'} ${name}`).join(' / ');
  const itemStats = result.items || { total_count: 0, ready_count: 0, blocked_count: 0, issue_counts: {}, blocked_items: [] };
  const issueRows = Object.entries(itemStats.issue_counts || {}).map(([issue, count]) => `${issue} × ${count}`).join(' / ') || '无';
  const warningRows = Object.entries(itemStats.warning_counts || {}).map(([warning, count]) => `${warning} × ${count}`).join(' / ') || '无';
  const blockedRows = (itemStats.blocked_items || []).slice(0, 5).map(item => `<div>⚠️ ${item.skc}：${(item.issues || []).join('；')}</div>`).join('') || '<div>全部商品字段通过</div>';
  const rpaImages = result.rpa_images || { prepared_count: 0, missing_count: 0, root: '' };
  const cos = result.cos || { image_source: 'local', config_exists: false, region: '', bucket: '', prefix: '' };
  preflightBox.innerHTML = `
    <div style="text-align:left; line-height:1.8;">
      <div><b>Script Dir: </b>${result.script_dir}</div>
      <div><b>Script Dir Exists: </b>${result.script_dir_exists ? '存在' : '缺失'}</div>
      <div><b>Scripts: </b>${scriptRows}</div>
      <div><b>Command Preview: </b>${result.command_preview || '-'}</div>
      <div><b>Latest Export: </b>${result.latest_export || 'None'}</div>
      <div><b>Image Dir: </b>${result.image_dir_exists ? '存在' : '缺失'} · ${result.image_dir}</div>
      <div><b>RPA 图片目录: </b>${rpaImages.root || result.rpa_image_dir || '-'} · 已准备 ${rpaImages.prepared_count || 0} 个，缺失 ${rpaImages.missing_count || 0} 个</div>
      <div><b>图片上传模式: </b>${cos.image_source === 'cos' ? 'COS 网络图' : '本地文件'} · ${cos.bucket || '未配置 Bucket'} ${cos.prefix ? `/${cos.prefix}` : ''}</div>
      <div><b>Infra: </b><span class="badge ${result.infra_ready ? 'green' : 'orange'}">${result.infra_ready ? '通过' : '需处理'}</span></div>
      <div><b>商品预检: </b>${itemStats.ready_count}/${itemStats.total_count} 可上货，${itemStats.blocked_count} 需处理</div>
      <div><b>阻断问题: </b>${issueRows}</div>
      <div><b>字段预警: </b>${warningRows}</div>
      <div>${blockedRows}</div>
      <div><b>Preflight: </b><span class="badge ${result.ready ? 'green' : 'orange'}">${result.ready ? '通过' : '需处理'}</span></div>
    </div>
  `;
  addOperationLog('上货预检', result.ready ? 'success' : 'error', result.ready ? '预检通过，可以进入创建任务/真实上货' : `预检未通过：${itemStats.blocked_count || 0} 个商品需处理`, result.ready ? 55 : 35);
}





async function realUpload() {
  addOperationLog('正式上货', 'running', '正在开始正式上货', 62);
  const response = await fetch('/api/upload-tasks/run', { method: 'POST' });
  const task = await response.json();
  await refreshOperationalViews();
  addOperationLog('正式上货', task.status === 'rpa_success' ? 'success' : (task.status === 'blocked' || task.status === 'needs_review' ? 'error' : 'info'), task.run_log || `任务状态：${task.status}`, task.status === 'rpa_success' ? 100 : 72);
  await notify(task.run_log || '正式上货已执行');
}

async function createUploadTask() {
  addOperationLog('保存上货设置', 'running', '正在保存本次上货操作设置', 50);
  await saveSettings({ silent: true });
  addOperationLog('保存上货设置', 'success', '设置已写入，创建任务时会生成设置快照', 56);
  addOperationLog('创建上货任务', 'running', '正在生成任务、导出表和 manifest 快照', 58);
  const response = await fetch('/api/upload-tasks', { method: 'POST' });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '创建上货任务失败');
    return;
  }
  await refreshOperationalViews();
  addOperationLog('创建上货任务', 'success', '任务已创建，可在任务列表查看日志和 manifest', 76);
  await notify('已创建上货任务');
}

async function deleteUploadTask(taskId) {
  if (!await askConfirm('确认删除这个上货任务吗？')) return;
  const response = await fetch(`/api/upload-tasks/${taskId}`, { method: 'DELETE' });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '删除任务失败');
    return;
  }
  await refreshOperationalViews();
}

async function clearUploadTasks() {
  if (!await askConfirm('确认清空全部上货任务和发布记录吗？')) return;
  const response = await fetch('/api/upload-tasks/clear', { method: 'POST' });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '清空任务失败');
    return;
  }
  await refreshOperationalViews();
}



async function refreshOperationalViews() {
  addOperationLog('刷新状态', 'running', '正在刷新任务、发布记录、缺图和预检状态', Math.max(operationProgress, 20));
  try {
    await loadDashboard();
    await loadProducts();
    await loadProcessingItems();
    await loadMissingImages();
    await loadUploadTasks();
    await loadPublishRecords();
    addOperationLog('刷新状态', 'success', '状态刷新完成', Math.max(operationProgress, 45));
  } catch (error) {
    addOperationLog('刷新状态', 'error', error.message, operationProgress || 20);
    await notify(`刷新失败：${error.message}`);
  }
}

async function batchUploadImages(event) {
  const files = Array.from(event.target.files || []);
  if (!files.length) return;
  const data = new FormData();
  files.forEach(file => data.append('images', file));
  const response = await fetch('/api/products/images/batch', { method: 'POST', body: data });
  const result = await response.json();
  await refreshOperationalViews();
  await notify(`Batch image upload done. Updated: ${result.updated_count}; Unmatched: ${result.unmatched_count}`);
  event.target.value = '';
}

function renderProducts() {
  if (!products.length) {
    productsBody.innerHTML = '<tr><td class="empty-row" colspan="13">暂无商品，点击“新增商品”开始录入</td></tr>';
    return;
  }
  productsBody.innerHTML = products.map(product => {
    const statusText = productStatusText(product.status);
    return `
      <tr>
        <td><input type="checkbox" data-product-select="${product.id}" /></td>
        <td>${product.title}</td>
        <td>${product.skc}</td>
        <td>${product.sku_summary || '-'}</td>
        <td>${product.main_image ? `<div class="thumb"><img src="${product.main_image}" alt="${product.title}"></div>` : '<span class="badge red">缺主图</span>'}</td>
        <td>${money(product.purchase_price)}</td>
        <td>${money(product.first_mile)}</td>
        <td>${money(product.platform_cost)}</td>
        <td>${money(product.total_cost)}</td>
        <td>${money(product.estimated_profit)}</td>
        <td><span class="badge ${product.gross_margin >= 38 ? 'green' : 'orange'}">${Number(product.gross_margin).toFixed(1)}%</span></td>
        <td><span class="badge ${statusClass(statusText)}">${statusText}</span></td>
        <td class="actions">
          <button class="btn ghost" data-edit="${product.id}">编辑</button>
          <label class="btn outline-blue file-label">主图<input type="file" accept="image/*" data-image="${product.id}" /></label>
          <button class="btn outline-blue" data-process-image="${product.id}">处理图</button>
          <button class="btn outline-blue" data-refresh-image="${product.id}">查图</button>
          <button class="btn outline-orange" data-delete="${product.id}">删除</button>
        </td>
      </tr>
    `;
  }).join('');
}

function renderCollectionItems() {
  if (!collectionBody) return;
  if (!collectionItems.length) {
    collectionBody.innerHTML = '<tr><td class="empty-row" colspan="8">暂无采集结果，请开始真实采集或导入 CSV/XLSX/JSON</td></tr>';
    return;
  }
  collectionBody.innerHTML = collectionItems.map(item => `
    <tr>
      <td><input type="checkbox" data-collection-id="${item.id}" data-collection-status="${item.status}"></td>
      <td>${item.image_url ? `<img class="thumb collection-thumb" src="${item.image_url}" alt="${item.title}" loading="lazy" referrerpolicy="no-referrer" data-preview-image="${item.image_url}" data-preview-title="${item.title}" onerror="this.onerror=null;this.src='/api/image-proxy?url=${encodeURIComponent(item.image_url)}';">` : '<span class="desc">无图</span>'}</td>
      <td>${item.source_url ? `<a href="${item.source_url}" target="_blank" rel="noopener">${item.title}</a>` : item.title}</td>
      <td>${item.source}</td>
      <td>${money(item.price)}</td>
      <td>${item.sales}</td>
      <td>${item.image_count} 张</td>
      <td><span class="badge ${item.status === 'imported' ? 'green' : 'orange'}">${collectionStatusText(item.status)}</span></td>
    </tr>
  `).join('');
}



function visibleProcessingItems() {
  const statusFilter = processingStatusFilter?.value || '';
  return statusFilter ? processingItems.filter(item => item.status === statusFilter) : processingItems;
}

function selectedProcessingProductIds() {
  const checkedIds = Array.from(document.querySelectorAll('[data-processing-check]:checked')).map(input => Number(input.dataset.processingCheck));
  const mergedIds = new Set([...selectedProcessingIds, ...checkedIds]);
  return Array.from(mergedIds).filter(id => processingItems.some(item => item.product_id === id));
}

function syncProcessingSelectAllState() {
  if (!selectAllProcessing) return;
  const visibleItems = visibleProcessingItems();
  const visibleIds = visibleItems.map(item => item.product_id);
  const checkedCount = visibleIds.filter(id => selectedProcessingIds.has(id)).length;
  selectAllProcessing.checked = Boolean(visibleIds.length && checkedCount === visibleIds.length);
  selectAllProcessing.indeterminate = Boolean(checkedCount && checkedCount < visibleIds.length);
}

function renderProcessingItems() {
  if (!processingBody) return;
  const visibleItems = visibleProcessingItems();
  if (!visibleItems.length) {
    processingBody.innerHTML = '<div class="empty-row">暂无商品处理数据，先从商品库或采集结果加入商品</div>';
    renderProcessingDetail(null);
    syncProcessingSelectAllState();
    return;
  }
  if (!selectedProcessingProductId || !visibleItems.some(item => item.product_id === selectedProcessingProductId)) {
    selectedProcessingProductId = visibleItems[0].product_id;
  }
  const visibleIds = new Set(visibleItems.map(item => item.product_id));
  selectedProcessingIds = new Set(Array.from(selectedProcessingIds).filter(id => visibleIds.has(id)));
  processingBody.innerHTML = visibleItems.map(item => {
    const imageOptions = item.image_options || [];
    const preview = item.main_image || imageOptions[0]?.preview_url || '';
    const checked = selectedProcessingIds.has(item.product_id) ? 'checked' : '';
    const cardClass = processingCardClass(item);
    return `
      <button class="processing-card ${cardClass} ${item.product_id === selectedProcessingProductId ? 'active' : ''}" data-processing-select="${item.product_id}">
        <input class="processing-select" type="checkbox" data-processing-check="${item.product_id}" ${checked} aria-label="选择商品 ${item.skc}">
        <span class="processing-card-delete" title="删除待处理商品" data-processing-delete="${item.product_id}">×</span>
        <div>${preview ? `<img src="${preview}" alt="${item.skc}" loading="lazy" referrerpolicy="no-referrer">` : '<span>无图</span>'}</div>
        <section>
          <strong>${item.skc}</strong>
          <p>${item.title}</p>
          <footer>${processingUploadBadge(item)}<span>${imageOptions.length} 图</span></footer>
        </section>
      </button>
  `;
  }).join('');
  syncProcessingSelectAllState();
  renderProcessingDetail(visibleItems.find(item => item.product_id === selectedProcessingProductId));
}


const COLOR_ALIAS_ENTRIES = [
  ["black", "Black"],
  ["\u9ed1", "Black"],
  ["\u9ed1\u8272", "Black"],
  ["\u7eaf\u9ed1", "Black"],
  ["blk", "Black"],
  ["white", "White"],
  ["\u767d", "White"],
  ["\u767d\u8272", "White"],
  ["\u7eaf\u767d", "White"],
  ["ivory", "White"],
  ["\u7c73\u767d", "White"],
  ["\u8c61\u7259\u767d", "White"],
  ["beige", "Beige"],
  ["\u7c73\u8272", "Beige"],
  ["\u674f\u8272", "Beige"],
  ["\u674f", "Beige"],
  ["apricot", "Beige"],
  ["cream", "Beige"],
  ["\u5976\u6cb9\u8272", "Beige"],
  ["khaki", "Khaki"],
  ["\u5361\u5176", "Khaki"],
  ["\u5361\u5176\u8272", "Khaki"],
  ["camel", "Khaki"],
  ["\u9a7c\u8272", "Khaki"],
  ["brown", "Brown"],
  ["\u68d5\u8272", "Brown"],
  ["\u68d5", "Brown"],
  ["\u5496\u5561\u8272", "Brown"],
  ["coffee", "Brown"],
  ["chocolate", "Brown"],
  ["\u5de7\u514b\u529b\u8272", "Brown"],
  ["gray", "Grey"],
  ["grey", "Grey"],
  ["\u7070", "Grey"],
  ["\u7070\u8272", "Grey"],
  ["lightgray", "Grey"],
  ["\u6d45\u7070", "Grey"],
  ["darkgray", "Grey"],
  ["\u6df1\u7070", "Grey"],
  ["silvergray", "Grey"],
  ["red", "Red"],
  ["\u7ea2", "Red"],
  ["\u7ea2\u8272", "Red"],
  ["winered", "Red"],
  ["\u9152\u7ea2", "Red"],
  ["burgundy", "Red"],
  ["\u67a3\u7ea2", "Red"],
  ["\u73ab\u7ea2", "Red"],
  ["rosered", "Red"],
  ["pink", "Pink"],
  ["\u7c89", "Pink"],
  ["\u7c89\u8272", "Pink"],
  ["\u6d45\u7c89", "Pink"],
  ["\u85d5\u7c89", "Pink"],
  ["hotpink", "Pink"],
  ["\u6843\u7ea2", "Pink"],
  ["orange", "Orange"],
  ["\u6a59", "Orange"],
  ["\u6a59\u8272", "Orange"],
  ["\u6854\u8272", "Orange"],
  ["yellow", "Yellow"],
  ["\u9ec4", "Yellow"],
  ["\u9ec4\u8272", "Yellow"],
  ["\u59dc\u9ec4", "Yellow"],
  ["\u660e\u9ec4", "Yellow"],
  ["gold", "Gold"],
  ["\u91d1\u8272", "Gold"],
  ["\u91d1", "Gold"],
  ["green", "Green"],
  ["\u7eff", "Green"],
  ["\u7eff\u8272", "Green"],
  ["armygreen", "Green"],
  ["\u519b\u7eff", "Green"],
  ["olive", "Green"],
  ["\u6a44\u6984\u7eff", "Green"],
  ["mintgreen", "Green"],
  ["\u8584\u8377\u7eff", "Green"],
  ["\u58a8\u7eff", "Green"],
  ["\u6d45\u7eff", "Green"],
  ["\u6df1\u7eff", "Green"],
  ["blue", "Blue"],
  ["\u84dd", "Blue"],
  ["\u84dd\u8272", "Blue"],
  ["navy", "Blue"],
  ["navyblue", "Blue"],
  ["\u85cf\u9752", "Blue"],
  ["\u85cf\u84dd", "Blue"],
  ["\u6df1\u84dd", "Blue"],
  ["skyblue", "Blue"],
  ["\u5929\u84dd", "Blue"],
  ["lightblue", "Blue"],
  ["\u6d45\u84dd", "Blue"],
  ["denimblue", "Blue"],
  ["\u725b\u4ed4\u84dd", "Blue"],
  ["\u5b9d\u84dd", "Blue"],
  ["\u6e56\u84dd", "Blue"],
  ["purple", "Purple"],
  ["\u7d2b", "Purple"],
  ["\u7d2b\u8272", "Purple"],
  ["lavender", "Purple"],
  ["\u85b0\u8863\u8349\u7d2b", "Purple"],
  ["violet", "Purple"],
  ["\u6d45\u7d2b", "Purple"],
  ["\u6df1\u7d2b", "Purple"],
  ["silver", "Silver"],
  ["\u94f6\u8272", "Silver"],
  ["\u94f6", "Silver"],
  ["multi", "Multicolor"],
  ["multicolor", "Multicolor"],
  ["\u5f69\u8272", "Multicolor"],
  ["\u82b1\u8272", "Multicolor"],
  ["\u62fc\u8272", "Multicolor"],
  ["clear", "Clear"],
  ["\u900f\u660e", "Clear"],
];
const COLOR_ALIAS_MAP = new Map(COLOR_ALIAS_ENTRIES.map(([alias, color]) => [normalizeColorToken(alias), color]));

function normalizeColorToken(value) {
  return String(value || '').toLowerCase().replace(/[\s\-_【】\[\]（）(){}:：,，/\\|;；]+/g, '');
}

function isImageUrl(url) {
  return /\.(jpg|jpeg|png|webp|gif)(\?|$)/i.test(String(url || ''));
}

function summarizeSpec(value) {
  if (!value || value === 'pending') return '待确认';
  const parts = String(value).split('/').map(item => item.trim()).filter(Boolean);
  return parts.length > 3 ? `${parts.slice(0, 3).join(' / ')} 等 ${parts.length} 项` : parts.join(' / ');
}

function normalizeKnownColor(value) {
  const text = String(value || '').trim();
  if (!text) return '';
  const direct = COLOR_ALIAS_MAP.get(normalizeColorToken(text));
  if (direct) return direct;
  const candidates = text.split(/[\r\n,，、/]+/).map(part => part.trim()).filter(Boolean);
  for (const candidate of candidates) {
    const color = COLOR_ALIAS_MAP.get(normalizeColorToken(candidate));
    if (color) return color;
  }
  for (const [alias, color] of COLOR_ALIAS_MAP.entries()) {
    if (alias && normalizeColorToken(text).includes(alias)) return color;
  }
  return '';
}

function cleanSpecLabel(value, type) {
  const text = String(value || '').trim();
  if (!text) return '';
  const pattern = type === 'color' ? /颜色[:：]([^;\/]+)/ : /尺码[:：]([^;\/]+)/;
  const match = text.match(pattern);
  const label = (match ? match[1] : text).replace(/[()（）]/g, '').trim();
  return type === 'color' ? normalizeKnownColor(label) : label;
}

function processingImageStats(item) {
  const options = item.image_options || [];
  const colorMap = new Map();
  let skuImageCount = 0;
  options.forEach(option => {
    if (option.kind === 'detail_sku_image' || option.color || option.size) {
      skuImageCount += 1;
      const color = cleanSpecLabel(option.color, 'color');
      if (!color) return;
      if (!colorMap.has(color)) colorMap.set(color, { color, imageCount: 0, sizes: new Set() });
      const entry = colorMap.get(color);
      entry.imageCount += 1;
      const size = cleanSpecLabel(option.size, 'size');
      if (size) entry.sizes.add(size);
    }
  });
  return {
    totalImages: options.length,
    skuImageCount,
    colors: Array.from(colorMap.values()).map(entry => ({ color: entry.color, imageCount: entry.imageCount, sizes: Array.from(entry.sizes) })),
  };
}

function imageIdentity(url) {
  const text = String(url || '').trim();
  if (!text) return '';
  try {
    const parsed = new URL(text, window.location.origin);
    return `${parsed.origin}${parsed.pathname}`;
  } catch (_) {
    return text.split('?')[0];
  }
}

function uniqueImageOptionsByUrl(options) {
  const seen = new Set();
  return options.filter(option => {
    const key = imageIdentity(option.url);
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function groupImageOptionsByColor(imageOptions) {
  const groups = new Map();
  imageOptions.forEach(option => {
    const color = cleanSpecLabel(option.color, 'color') || (option.kind === 'main_image' ? '商品主图' : option.kind === 'detail_main_image' ? '详情图' : '未归类图片');
    if (!groups.has(color)) groups.set(color, []);
    groups.get(color).push(option);
  });
  return Array.from(groups.entries()).map(([color, options]) => ({ color, options: uniqueImageOptionsByUrl(options) }));
}

function uniqueList(values) {
  return Array.from(new Set(values));
}

function splitSpecList(value, type) {
  const splitter = type === 'color' ? /[\r\n,，、/]+/ : /[\/|,，、;；]+/;
  return uniqueList((String(value || '').split(splitter).map(part => cleanSpecLabel(part, type)).filter(Boolean)));
}

function buildVariantMatrix(item, imageOptions) {
  const colorMap = new Map();
  const globalColors = splitSpecList(item.color, 'color');
  const globalSizes = splitSpecList(item.size, 'size');
  const ensureColor = color => {
    const key = cleanSpecLabel(color, 'color');
    if (!key) return null;
    if (!colorMap.has(key)) colorMap.set(key, { color: key, images: [], imageUrls: new Set(), sizes: new Set(), skuIds: new Set() });
    return colorMap.get(key);
  };
  globalColors.forEach(color => ensureColor(color));
  imageOptions.filter(option => option.color || option.size || option.sku_id).forEach(option => {
    const color = cleanSpecLabel(option.color, 'color') || globalColors[0] || '';
    const entry = ensureColor(color);
    if (!entry) return;
    const size = cleanSpecLabel(option.size, 'size');
    if (size) entry.sizes.add(size);
    if (option.sku_id) entry.skuIds.add(option.sku_id);
    if (option.url && !entry.imageUrls.has(option.url)) {
      entry.imageUrls.add(option.url);
      entry.images.push(option);
    }
  });
  if (!colorMap.size) return { colors: [], sizes: globalSizes, rows: [] };
  const colorEntries = Array.from(colorMap.values()).map(entry => ({
    color: entry.color,
    images: entry.images,
    sizes: Array.from(entry.sizes),
    skuIds: Array.from(entry.skuIds),
  }));
  const allSizes = uniqueList([...globalSizes, ...colorEntries.flatMap(entry => entry.sizes)]);
  const rows = colorEntries.flatMap(entry => {
    const sizes = allSizes.length ? allSizes : (entry.sizes.length ? entry.sizes : ['待识别']);
    return sizes.map(size => ({ color: entry.color, size, image: entry.images[0] || null }));
  });
  return { colors: colorEntries, sizes: allSizes, rows };
}

function renderProcessingDetail(item) {
  if (!processingDetailPanel) return;
  if (!item) {
    if (processingDetailStatus) processingDetailStatus.textContent = '未选择';
    processingDetailPanel.innerHTML = '<div class="empty-row">请选择左侧商品</div>';
    return;
  }
  if (processingDetailStatus) {
    const readiness = processingColorReadiness(item);
    processingDetailStatus.textContent = readiness.ready ? '可导出' : '需补图';
    processingDetailStatus.className = `badge ${readiness.ready ? 'green' : 'red'}`;
  }
  const imageOptions = item.image_options || [];
  const selectedImage = imageOptions.find(option => option.kind === 'detail_sku_image')?.url || imageOptions.find(option => option.kind !== 'main_image' && isImageUrl(option.url))?.url || imageOptions.find(option => isImageUrl(option.url))?.url || imageOptions[0]?.url || '';
  const selectedOption = imageOptions.find(option => option.url === selectedImage);
  if (!selectedProcessingImageUrls.has(item.product_id)) {
    selectedProcessingImageUrls.set(item.product_id, new Set(selectedImage ? [selectedImage] : []));
  }
  const selectedImageUrls = selectedProcessingImageUrls.get(item.product_id);
  const skuOptions = imageOptions.filter(option => option.color || option.size || option.sku_id);
  const stats = processingImageStats(item);
  const matrix = buildVariantMatrix(item, imageOptions);
  const descOptions = uniqueImageOptionsByUrl(imageOptions.filter(option => option.kind === 'detail_desc_image'));
  const productDisplayImageOptions = uniqueImageOptionsByUrl(imageOptions.filter(option => !option.color && !option.size && !option.sku_id && option.kind !== 'detail_sku_image'));
  const productDisplayImageCards = productDisplayImageOptions.length
    ? productDisplayImageOptions.map((option, index) => {
      const imageSrc = option.preview_url || option.url;
      const selected = option.url === selectedImage;
      const colorLabel = cleanSpecLabel(option.color, 'color');
      const sizeLabel = cleanSpecLabel(option.size, 'size');
      const kindLabel = option.kind === 'main_image' ? '商品主图' : option.kind === 'detail_main_image' ? '详情/轮播图' : option.kind === 'detail_desc_image' ? '详情图' : option.kind === 'detail_sku_image' ? '颜色图' : option.kind === 'collection_image' ? '采集图' : option.kind === 'local_file' ? '本地图' : '图片';
      const label = [colorLabel, sizeLabel].filter(Boolean).join(' / ') || `${kindLabel} #${index + 1}`;
      return `<button class="carousel-image ${selected ? 'active' : ''}" draggable="true" data-draggable-image="true" data-image-url="${option.url}"><img src="${imageSrc}" alt="${label}" loading="lazy" referrerpolicy="no-referrer" data-preview-image="${imageSrc}" data-preview-title="${label}"><span>${label}</span></button>`;
    }).join('')
    : '<div class="desc">暂无轮播图/详情图</div>'; 
  const assignmentsByColor = new Map();
  (item.color_image_assignments || []).forEach(assignment => {
    const color = cleanSpecLabel(assignment.color, 'color');
    if (!color) return;
    if (!assignmentsByColor.has(color)) assignmentsByColor.set(color, []);
    assignmentsByColor.get(color).push(assignment);
  });
  const colorImageRows = matrix.colors.length
    ? matrix.colors.map(entry => {
      const assignedImages = assignmentsByColor.get(entry.color) || [];
      const slotImages = Array.from({ length: 5 }, (_slot, index) => assignedImages.find(option => Number(option.sort_order) === index) || assignedImages[index] || null);
      return `<div class="skc-row"><div class="skc-color"><b>${entry.color}</b><small>${assignedImages.length ? `已分图 ${assignedImages.length} / 5 张` : (entry.sizes.length ? entry.sizes.join(' / ') : '尺码待识别')}</small></div><div class="skc-code">${item.skc}-${entry.color}</div><div class="skc-images skc-slots">${slotImages.map((option, index) => {
        if (!option) return `<button class="skc-image skc-slot empty" data-skc-drop-slot="true" data-product-id="${item.product_id}" data-color="${entry.color}" data-slot-index="${index}" aria-label="添加${entry.color}颜色图 #${index + 1}"><span class="slot-title">#${index + 1}</span><em>拖入或点击加号</em><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="选择图片">+</strong></button>`;
        const imageUrl = option.image_url || option.url;
        const imageSrc = option.preview_url || option.previewUrl || imageUrl;
        const selected = selectedImageUrls.has(imageUrl);
        return `<button class="skc-image skc-slot image-select-card ${selected ? 'active' : ''}" data-skc-drop-slot="true" data-product-id="${item.product_id}" data-color="${entry.color}" data-slot-index="${index}" data-processing-image-pick="${item.product_id}" data-image-url="${imageUrl}" aria-label="${entry.color}颜色图 #${index + 1}"><i class="image-select-check">✓</i><img src="${imageSrc}" alt="${entry.color} #${index + 1}" loading="lazy" referrerpolicy="no-referrer" data-preview-image="${imageSrc}" data-preview-title="${entry.color} #${index + 1}"><span class="slot-title">#${index + 1}</span><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="更换图片">+</strong><i class="slot-action slot-delete" data-clear-skc-slot="true" aria-label="删除图片">×</i></button>`;
      }).join('')}</div></div>`;
    }).join('')
    : '<div class="desc">暂未识别颜色图片</div>';
  const sizeChips = matrix.sizes.length
    ? matrix.sizes.map(size => `<span class="size-chip active">✓ ${size}</span>`).join('')
    : '<span class="desc">尺码待识别</span>';
  const variantRows = matrix.rows.length
    ? matrix.rows.map(row => `<tr><td>${row.color}</td><td>${row.size}</td><td>${item.skc}-${row.color}-${row.size}</td><td>${row.image ? '<span class="badge green">有图</span>' : '<span class="badge red">待补图</span>'}</td><td>${Number(item.declared_price).toFixed(2)}</td><td>${item.stock}</td></tr>`).join('')
    : '<tr><td class="empty-row" colspan="6">暂无变种明细</td></tr>';
  const detailAssignments = item.detail_image_assignments || [];
  const detailOptions = detailAssignments.length ? detailAssignments : descOptions;
  const visibleDetailOptions = detailOptions
    .map((option, index) => ({ option, index }))
    .filter(({ option }) => option && (option.image_url || option.url));
  const detailCards = visibleDetailOptions.map(({ option, index }, displayIndex) => {
    const imageUrl = option.image_url || option.url || '';
    const imageSrc = option.preview_url || option.previewUrl || imageUrl;
    const selected = selectedImageUrls.has(imageUrl);
    return `<button class="carousel-image detail-slot image-select-card ${selected ? 'active' : ''}" draggable="true" data-draggable-image="true" data-detail-drop-slot="true" data-product-id="${item.product_id}" data-slot-index="${index}" data-processing-image-pick="${item.product_id}" data-image-url="${imageUrl}" aria-label="详情图 #${displayIndex + 1}"><i class="image-select-check">✓</i><img src="${imageSrc}" alt="详情图 #${displayIndex + 1}" loading="lazy" referrerpolicy="no-referrer" data-preview-image="${imageSrc}" data-preview-title="详情图 #${displayIndex + 1}"><span class="slot-title">详情图 #${displayIndex + 1}</span><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="更换图片">+</strong><i class="slot-action slot-delete" data-clear-detail-slot="true" aria-label="删除图片">×</i></button>`;
  }).join('');
  const nextDetailSlotIndex = Math.max(-1, ...visibleDetailOptions.map(({ index }) => Number(index))) + 1;
  const addDetailCard = `<button class="carousel-image detail-slot empty detail-add-slot" data-detail-drop-slot="true" data-product-id="${item.product_id}" data-slot-index="${nextDetailSlotIndex}" aria-label="添加详情图"><span class="slot-title">添加详情图</span><small>拖入图片或点击加号选择</small><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="选择图片">+</strong></button>`;
  const detailSlotCount = visibleDetailOptions.length;
  processingDetailPanel.innerHTML = `
    <div class="processing-detail-grid">
      <section class="detail-block wide"><h3>基础信息</h3><div class="kv"><span>商品标题</span><b>${item.title}</b></div><div class="kv"><span>英文标题</span><b>${item.english_title}</b></div><div class="kv"><span>SKC</span><b>${item.skc}</b></div><div class="kv"><span>站外链接</span><b>${item.source_url ? `<a href="${item.source_url}" target="_blank" rel="noopener">打开详情</a>` : '无'}</b></div></section>
      <section class="detail-block wide"><h3>轮播图与详情图</h3><div class="image-picker-toolbar"><input type="hidden" data-processing-image-source="${item.product_id}" value="${selectedImage}"><span class="desc">仅展示商品轮播图 + 商品详情图，不参与多选；颜色图和详情图请在下方槽位里选择</span><span class="badge blue">${productDisplayImageOptions.length} 张</span></div><div class="carousel-image-list">${productDisplayImageCards}</div></section>
      <section class="detail-block wide"><h3>变种属性</h3><div class="spec-summary"><span>颜色 <b>${matrix.colors.length || '待识别'}</b></span><span>尺码 <b>${matrix.sizes.length || '待识别'}</b></span><span>变种 <b>${matrix.rows.length || '待识别'}</b></span><span>SKU图 <b>${stats.skuImageCount} / ${stats.totalImages}</b></span></div><div class="skc-manager"><div class="skc-manager-head"><b>全部 SKU 颜色图片管理</b><span>每个颜色最多 5 张 · 首图作为该颜色封面 · 点击任意图可用于图生图</span><div class="skc-manager-actions"><button class="btn ghost" data-auto-assign-images="${item.product_id}" data-count="3">自动分图 3张</button><button class="btn ghost" data-auto-assign-images="${item.product_id}" data-count="5">自动分图 5张</button><button class="btn outline-blue" data-auto-assign-images="${item.product_id}" data-count="5" data-use-vision="true">识别分图 5张</button></div></div>${colorImageRows}</div><div class="size-manager"><div class="skc-manager-head"><b>尺码设置</b><span>从商品详情页自动识别</span></div><div class="size-chip-list">${sizeChips}</div></div></section>
      <section class="detail-block wide"><h3>变种明细</h3><div class="variant-table-wrap"><table class="variant-table"><thead><tr><th>颜色</th><th>尺码</th><th>SKU 货号预览</th><th>图片</th><th>申报价</th><th>库存</th></tr></thead><tbody>${variantRows}</tbody></table></div></section>
      <section class="detail-block wide"><h3>商品详情图</h3><div class="image-picker-toolbar"><span class="desc">只显示已有详情图；最后一个卡片用于添加或拖入新图</span><span class="badge blue">${detailSlotCount} 张</span></div><div class="carousel-image-list detail-slot-list">${detailCards}${addDetailCard}</div></section>
      <section class="detail-block wide muted-block"><h3>上货字段摘要</h3><div class="spec-summary"><span>申报价 <b>${Number(item.declared_price).toFixed(2)}</b></span><span>重量 <b>${item.weight_g}g</b></span><span>尺寸 <b>${item.length_cm} × ${item.width_cm} × ${item.height_cm}cm</b></span><span>库存/发货 <b>${item.stock} / ${item.ship_days}天</b></span></div></section>
    </div>
  `;
}

function slotPickerLabel(option, index) {
  const colorLabel = cleanSpecLabel(option.color, 'color');
  const sizeLabel = cleanSpecLabel(option.size, 'size');
  const kindLabel = option.kind === 'main_image' ? '商品主图' : option.kind === 'detail_main_image' ? '轮播图' : option.kind === 'detail_desc_image' ? '详情图' : option.kind === 'detail_sku_image' ? '颜色图' : option.kind === 'collection_image' ? '采集图' : option.kind === 'local_file' ? '本地图' : '图片';
  return [colorLabel, sizeLabel].filter(Boolean).join(' / ') || `${kindLabel} #${index + 1}`;
}

function openSlotImagePicker(slot) {
  if (!slotImagePickerModal || !slotImagePickerGrid) return;
  const productId = Number(slot.dataset.productId || 0);
  const item = processingItems.find(current => current.product_id === productId);
  if (!item) return;
  const isDetail = slot.dataset.detailDropSlot === 'true';
  pendingSlotImagePick = {
    productId,
    slotIndex: Number(slot.dataset.slotIndex || 0),
    color: slot.dataset.color || '',
    isDetail,
  };
  pendingSlotImageUrls = new Set();
  const title = isDetail ? '选择详情图' : `选择颜色图：${pendingSlotImagePick.color || '未识别颜色'}`;
  if (slotImagePickerTitle) slotImagePickerTitle.textContent = title;
  if (slotImagePickerHint) slotImagePickerHint.textContent = isDetail ? '可多选，确认后从当前详情图槽位开始连续填入' : '可多选，确认后从当前颜色图槽位开始连续填入';
  const options = uniqueImageOptionsByUrl((item.image_options || []).filter(option => isImageUrl(option.url)));
  if (slotImagePickerCount) slotImagePickerCount.textContent = `已选 0 / ${options.length} 张`;
  slotImagePickerGrid.innerHTML = options.length ? options.map((option, index) => {
    const imageSrc = option.preview_url || option.previewUrl || option.url;
    const label = slotPickerLabel(option, index);
    return `<button class="slot-picker-card" type="button" data-slot-picker-url="${option.url}"><i class="image-select-check">✓</i><img src="${imageSrc}" alt="${label}" loading="lazy" referrerpolicy="no-referrer"><span>${label}</span></button>`;
  }).join('') : '<div class="empty-row">暂无可选图片</div>';
  slotImagePickerModal.classList.remove('hidden');
}

function closeSlotImagePicker() {
  slotImagePickerModal?.classList.add('hidden');
  pendingSlotImagePick = null;
  pendingSlotImageUrls = new Set();
}

function toggleSlotPickerImage(imageUrl) {
  if (!pendingSlotImagePick || !imageUrl) return;
  if (pendingSlotImageUrls.has(imageUrl)) pendingSlotImageUrls.delete(imageUrl);
  else pendingSlotImageUrls.add(imageUrl);
  slotImagePickerGrid?.querySelectorAll('[data-slot-picker-url]').forEach(card => {
    card.classList.toggle('selected', pendingSlotImageUrls.has(card.dataset.slotPickerUrl || ''));
  });
  const total = slotImagePickerGrid?.querySelectorAll('[data-slot-picker-url]').length || 0;
  if (slotImagePickerCount) slotImagePickerCount.textContent = `已选 ${pendingSlotImageUrls.size} / ${total} 张`;
}

async function confirmSlotPickerImages() {
  if (!pendingSlotImagePick || !pendingSlotImageUrls.size) {
    await notify('请先勾选图片');
    return;
  }
  const pick = pendingSlotImagePick;
  const urls = Array.from(pendingSlotImageUrls);
  closeSlotImagePicker();
  for (let index = 0; index < urls.length; index += 1) {
    const slotIndex = pick.slotIndex + index;
    if (pick.isDetail) await saveManualDetailImageAssignment(pick.productId, slotIndex, urls[index]);
    else await saveManualColorImageAssignment(pick.productId, pick.color, slotIndex, urls[index]);
  }
}

function openImagePreview(src, title) {
  if (!imagePreviewModal || !imagePreviewImg || !imagePreviewLink) return;
  imagePreviewImg.src = src;
  imagePreviewImg.referrerPolicy = 'no-referrer';
  imagePreviewImg.onerror = () => {
    imagePreviewImg.onerror = null;
    imagePreviewImg.src = `/api/image-proxy?url=${encodeURIComponent(src)}`;
  };
  imagePreviewTitle.textContent = title || '商品图片';
  imagePreviewLink.href = src;
  imagePreviewModal.classList.remove('hidden');
}

function positionHoverImagePreview(event) {
  if (!hoverImagePreview) return;
  const gap = 18;
  const previewWidth = hoverImagePreview.offsetWidth || 300;
  const previewHeight = hoverImagePreview.offsetHeight || 300;
  let left = event.clientX + gap;
  let top = event.clientY + gap;
  if (left + previewWidth > window.innerWidth - 12) left = event.clientX - previewWidth - gap;
  if (top + previewHeight > window.innerHeight - 12) top = window.innerHeight - previewHeight - 12;
  hoverImagePreview.style.left = `${Math.max(12, left)}px`;
  hoverImagePreview.style.top = `${Math.max(12, top)}px`;
}

function showHoverImagePreview(event, target) {
  if (!hoverImagePreview || !hoverImagePreviewImg) return;
  const src = target.dataset.previewImage;
  if (!src) return;
  hoverImagePreviewImg.src = src;
  hoverImagePreviewImg.referrerPolicy = 'no-referrer';
  hoverImagePreviewImg.onerror = () => {
    hoverImagePreviewImg.onerror = null;
    hoverImagePreviewImg.src = `/api/image-proxy?url=${encodeURIComponent(src)}`;
  };
  positionHoverImagePreview(event);
  hoverImagePreview.classList.remove('hidden');
}

function hideHoverImagePreview() {
  if (!hoverImagePreview) return;
  hoverImagePreview.classList.add('hidden');
}

function selectedProductIds() {
  return Array.from(document.querySelectorAll('[data-product-select]:checked')).map(input => Number(input.dataset.productSelect));
}

async function updateSelectedProductsStatus() {
  const ids = selectedProductIds();
  if (!ids.length) {
    await notify('请选择商品');
    return;
  }
  const response = await fetch('/api/products/bulk/status', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids, status: bulkProductStatus.value }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '批量改状态失败');
    return;
  }
  await refreshOperationalViews();
}

async function deleteSelectedProducts() {
  const ids = selectedProductIds();
  if (!ids.length) {
    await notify('请选择商品');
    return;
  }
  if (!await askConfirm(`确认删除选中的 ${ids.length} 个商品吗？对应主图也会删除。`)) return;
  const response = await fetch('/api/products/bulk/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '批量删除失败');
    return;
  }
  await refreshOperationalViews();
}

function renderCollectionTasks() {
  if (!collectionTasksBody) return;
  if (!collectionTasks.length) {
    collectionTasksBody.innerHTML = '<tr><td class="empty-row" colspan="12">暂无采集任务，填写配置后点击“开始采集”</td></tr>';
    return;
  }
  const executableStatuses = ['external_pending', 'blocked', 'empty', 'failed'];
  collectionTasksBody.innerHTML = collectionTasks.map(task => `
    <tr>
      <td>${task.id}</td>
      <td>${task.keyword}</td>
      <td>${task.source}</td>
      <td><span class="badge ${collectionTaskStatusClass(task.status)}">${collectionStatusText(task.status)}</span></td>
      <td>${task.target_count}</td>
      <td>${task.result_count || 0}</td>
      <td>${task.result_count || 0}</td>
      <td>-</td>
      <td>-</td>
      <td>${task.status === 'failed' ? 1 : 0}</td>
      <td>${task.created_at}</td>
      <td>${task.mode === '1688' && executableStatuses.includes(task.status) ? `<button class="btn ghost" data-collection-execute="${task.id}">重试</button>` : '-'}</td>
    </tr>
  `).join('');
}

function openProcessingForm(item) {
  if (!item || !processingModal) return;
  processingFormMode = 'single';
  if (processingSourceLabel) processingSourceLabel.textContent = '站外链接';
  const sourceInput = byId('processingSourceUrl');
  if (sourceInput) sourceInput.placeholder = 'https://...';
  byId('processingFormTitle').textContent = `编辑处理字段：${item.skc}`;
  byId('processingProductId').value = item.product_id;
  byId('processingDeclaredPrice').value = item.declared_price || 0;
  byId('processingWeightG').value = item.weight_g || 350;
  byId('processingLengthCm').value = item.length_cm || 15;
  byId('processingWidthCm').value = item.width_cm || 10;
  byId('processingHeightCm').value = item.height_cm || 2;
  byId('processingStock').value = item.stock || 999;
  byId('processingShipDays').value = item.ship_days || 9;
  byId('processingSourceUrl').value = item.source_url || '';
  processingModal.classList.remove('hidden');
}

function openBatchProcessingForm() {
  const ids = selectedProcessingProductIds();
  if (!ids.length) {
    notify('请先选择要批量编辑的商品');
    return;
  }
  processingFormMode = 'bulk';
  if (processingSourceLabel) processingSourceLabel.textContent = '起始 SKC';
  const sourceInput = byId('processingSourceUrl');
  if (sourceInput) sourceInput.placeholder = '例如 DS260504001，后续自动递增';
  byId('processingFormTitle').textContent = `批量编辑字段：${ids.length} 个商品`;
  byId('processingProductId').value = ids.join(',');
  byId('processingDeclaredPrice').value = 0;
  byId('processingWeightG').value = 350;
  byId('processingLengthCm').value = 15;
  byId('processingWidthCm').value = 10;
  byId('processingHeightCm').value = 2;
  byId('processingStock').value = 999;
  byId('processingShipDays').value = 9;
  byId('processingSourceUrl').value = '';
  processingModal.classList.remove('hidden');
}

function closeProcessingForm() {
  processingModal?.classList.add('hidden');
  processingForm?.reset();
  if (processingSourceLabel) processingSourceLabel.textContent = '站外链接';
  const sourceInput = byId('processingSourceUrl');
  if (sourceInput) sourceInput.placeholder = 'https://...';
  processingFormMode = 'single';
}

function processingPayload() {
  const productIds = String(byId('processingProductId').value || '').split(',').map(Number).filter(Boolean);
  const sourceItem = processingItems.find(item => item.product_id === productIds[0]) || {};
  const sourceValue = byId('processingSourceUrl').value.trim();
  return {
    english_title: sourceItem.english_title || '',
    sku_code: sourceItem.sku_code || '',
    color: sourceItem.color || '',
    size: sourceItem.size || '',
    declared_price: Number(byId('processingDeclaredPrice').value || 0),
    weight_g: Number(byId('processingWeightG').value || 350),
    length_cm: Number(byId('processingLengthCm').value || 15),
    width_cm: Number(byId('processingWidthCm').value || 10),
    height_cm: Number(byId('processingHeightCm').value || 2),
    source_url: processingFormMode === 'bulk' ? (sourceItem.source_url || '') : sourceValue,
    stock: Number(byId('processingStock').value || 999),
    ship_days: Number(byId('processingShipDays').value || 9),
  };
}
async function loadProcessingItems(options = {}) {
  if (!processingBody) return;
  const showFeedback = Boolean(options.feedback);
  const originalText = refreshProcessingButton?.textContent || '';
  if (showFeedback && refreshProcessingButton) {
    refreshProcessingButton.disabled = true;
    refreshProcessingButton.textContent = '刷新中...';
  }
  try {
    processingItems = await fetchJson('/api/processing-items');
    renderProcessingItems();
    if (showFeedback) await notify(`商品处理已刷新，共 ${processingItems.length} 条`);
  } catch (error) {
    if (showFeedback) await notify(`刷新失败：${error.message || error}`);
    else throw error;
  } finally {
    if (showFeedback && refreshProcessingButton) {
      refreshProcessingButton.disabled = false;
      refreshProcessingButton.textContent = originalText || '刷新';
    }
  }
}

async function loadProducts() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) params.set('q', searchInput.value.trim());
  if (productStatusFilter?.value) params.set('status', productStatusFilter.value);
  if (productImageFilter?.value) params.set('image', productImageFilter.value);
  products = await fetchJson(`/api/products${params.toString() ? `?${params}` : ''}`);
  renderProducts();
}

async function loadCollectionItems() {
  if (!collectionBody) return;
  const params = new URLSearchParams();
  const filterMap = {
    q: 'collectionSearchInput',
    source: 'collectionSourceFilter',
    status: 'collectionStatusFilter',
    min_price: 'collectionMinPriceFilter',
    max_price: 'collectionMaxPriceFilter',
    sort: 'collectionSortFilter',
  };
  Object.entries(filterMap).forEach(([key, id]) => {
    const value = byId(id)?.value?.trim();
    if (value) params.set(key, value);
  });
  collectionItems = await fetchJson(`/api/collection-items${params.toString() ? `?${params}` : ''}`);
  renderCollectionItems();
}

function selectedCollectionIds() {
  return Array.from(document.querySelectorAll('[data-collection-id]:checked')).map(input => Number(input.dataset.collectionId));
}

async function loadCollectionTasks() {
  if (!collectionTasksBody) return;
  collectionTasks = await fetchJson('/api/collection-tasks');
  renderCollectionTasks();
  const latest = collectionTasks[0];
  if (latest) {
    const logKey = `${latest.id}:${latest.status}:${latest.result_count}:${latest.note}`;
    if (logKey !== lastCollectionTaskLogKey) {
      lastCollectionTaskLogKey = logKey;
      const type = latest.status === 'completed' || latest.status === 'imported' ? 'success' : (latest.status === 'empty' || latest.status === 'failed' || latest.status === 'blocked' ? 'error' : 'info');
      addCollectionProgressLog('刷新任务列表', type, `最新任务 #${latest.id}：${collectionStatusText(latest.status)}，结果 ${latest.result_count || 0} 条。${latest.note || ''}`);
    }
  }
}

async function openCollectionRequest(taskId) {
  const response = await fetch(`/api/collection-tasks/${taskId}/request`);
  const result = await response.json();
  collectionRequestContent.textContent = `Path: ${result.path || '无'}\n\n${JSON.stringify(result.content || {}, null, 2)}`;
  collectionRequestModal.classList.remove('hidden');
}

async function clearCollectionTasks() {
  if (!await askConfirm('确认清空采集任务历史记录吗？不会删除已采集的候选商品。')) return;
  const response = await fetch('/api/collection-tasks/clear', { method: 'POST' });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '清空采集任务失败');
    return;
  }
  const result = await response.json();
  collectionTasks = [];
  lastCollectionTaskLogKey = '';
  renderCollectionTasks();
  addCollectionProgressLog('清空历史记录', 'success', `已清空 ${result.deleted_count || 0} 条采集任务历史`);
  await notify(`已清空 ${result.deleted_count || 0} 条采集任务历史，采集结果不受影响。`);
}

async function executeCollectionTask(taskId) {
  if (!await askConfirm('确认执行外部采集任务？如果外部采集执行开关未开启，本次会被安全阻断并记录原因。')) return;
  addCollectionProgressLog('执行采集任务', 'running', `正在执行任务 #${taskId}，结果会写入采集任务列表`);
  const response = await fetch(`/api/collection-tasks/${taskId}/execute`, { method: 'POST' });
  if (!response.ok) {
    const error = await response.json();
    addCollectionProgressLog('执行采集任务', 'error', error.detail || '执行采集任务失败');
    await notify(error.detail || '执行采集任务失败');
    return;
  }
  const task = await response.json();
  await loadCollectionTasks();
  await loadCollectionItems();
  addCollectionProgressLog('执行采集任务', ['completed', 'imported'].includes(task.status) ? 'success' : 'info', task.note || `采集任务状态：${collectionStatusText(task.status)}`);
  await notify(task.note || `采集任务状态：${collectionStatusText(task.status)}`);
}

function chooseCollectionResultFile(taskId) {
  pendingCollectionResultTaskId = taskId;
  collectionResultFileInput?.click();
}

async function importCollectionTaskResult(event) {
  const file = event.target.files?.[0];
  if (!file || !pendingCollectionResultTaskId) return;
  const data = new FormData();
  data.append('file', file);
  addCollectionProgressLog('回填采集结果', 'running', `正在解析并回填文件：${file.name}`);
  const response = await fetch(`/api/collection-tasks/${pendingCollectionResultTaskId}/import-result`, { method: 'POST', body: data });
  event.target.value = '';
  pendingCollectionResultTaskId = null;
  if (!response.ok) {
    const error = await response.json();
    addCollectionProgressLog('回填采集结果', 'error', error.detail || '回填采集结果失败');
    await notify(error.detail || '回填采集结果失败');
    return;
  }
  const task = await response.json();
  await loadCollectionTasks();
  await loadCollectionItems();
  addCollectionProgressLog('回填采集结果', 'success', task.note || '采集结果已回填');
  await notify(task.note || '采集结果已回填');
}

function collectionTaskPayload() {
  return {
    keyword: byId('collectionKeyword').value.trim(),
    source: byId('collectionSource').value,
    mode: byId('collectionMode')?.value || '1688',
    collector: byId('collectionMode')?.value || '1688',
    target_count: Number(byId('collectionTargetCount').value || 8),
    min_price: Number(byId('collectionMinPrice').value || 0),
    max_price: Number(byId('collectionMaxPrice').value || 0),
    blacklist: byId('collectionBlacklist').value.trim(),
  };
}

async function startCollectionTask() {
  const payload = collectionTaskPayload();
  addCollectionProgressLog('开始采集', 'running', `已提交关键词「${payload.keyword || '-'}」的采集请求，采集和解析会继续执行，请在任务列表查看状态`);
  const response = await fetch('/api/collection-tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json();
    addCollectionProgressLog('开始采集', 'error', error.detail || '创建采集任务失败');
    await notify(error.detail || '创建采集任务失败');
    return;
  }
  const task = await response.json();
  await loadCollectionTasks();
  await loadCollectionItems();
  addCollectionProgressLog('开始采集', 'success', `任务 #${task.id} 已开始/已记录，当前状态：${collectionStatusText(task.status)}。数量较多时请稍后刷新任务列表查看结果。`);
  await notify(`采集任务已开始。\n关键词：${task.keyword}\n任务状态：${collectionStatusText(task.status)}\n数量较多时不会立刻完成，请在“采集任务”和“采集执行日志”里查看进度。`);
}

async function importCollectionFile(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  const data = new FormData();
  data.append('source', collectionFileSource?.value || '外部文件');
  data.append('file', file);
  const response = await fetch('/api/collection-items/import-file', { method: 'POST', body: data });
  event.target.value = '';
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '导入采集文件失败');
    return;
  }
  const result = await response.json();
  await loadCollectionItems();
  await notify(`已导入 ${result.imported_count} 条候选商品，跳过 ${result.skipped_count} 条`);
}

function openForm(product = null) {
  formTitle.textContent = product ? '编辑商品' : '新增商品';
  document.querySelector('#productId').value = product?.id || '';
  document.querySelector('#title').value = product?.title || '';
  document.querySelector('#skc').value = product?.skc || '';
  document.querySelector('#skuSummary').value = product?.sku_summary || '';
  document.querySelector('#status').value = productStatusText(product?.status || '利润正常');
  document.querySelector('#purchasePrice').value = product?.purchase_price || 0;
  document.querySelector('#firstMile').value = product?.first_mile || 0;
  document.querySelector('#platformCost').value = product?.platform_cost || 0;
  modal.classList.remove('hidden');
}

function closeForm() {
  modal.classList.add('hidden');
  productForm.reset();
}

function formPayload() {
  return {
    title: document.querySelector('#title').value.trim(),
    skc: document.querySelector('#skc').value.trim(),
    sku_summary: document.querySelector('#skuSummary').value.trim(),
    status: document.querySelector('#status').value,
    purchase_price: Number(document.querySelector('#purchasePrice').value || 0),
    first_mile: Number(document.querySelector('#firstMile').value || 0),
    platform_cost: Number(document.querySelector('#platformCost').value || 0),
  };
}

async function importSelectedCollectionItems() {
  const ids = selectedCollectionIds();
  if (!ids.length) {
    await notify('请选择要加入商品库的采集结果');
    return;
  }
  const selectedItems = collectionItems.filter(item => ids.includes(item.id));
  const missingImageItems = selectedItems.filter(item => !item.image_url);
  const previewLines = selectedItems.slice(0, 6).map((item, index) => `${index + 1}. ${item.title || '未命名商品'}`);
  const moreText = selectedItems.length > previewLines.length ? `\n……另有 ${selectedItems.length - previewLines.length} 条` : '';
  const missingText = missingImageItems.length ? `\n\n其中 ${missingImageItems.length} 条没有主图，建议先补图，否则进入商品处理后仍会显示需补图。` : '';
  const confirmed = await askConfirm(
    `确认将 ${selectedItems.length} 条采集结果加入商品库？\n\n${previewLines.join('\n')}${moreText}${missingText}`,
    '加入商品库确认'
  );
  if (!confirmed) return;
  const response = await fetch('/api/collection-items/import', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '加入商品库失败');
    return;
  }
  await notify('已加入商品库');
  await loadCollectionItems();
  await loadProducts();
  await loadProcessingItems();
loadUploadTasks();
loadPublishRecords();
}

async function updateSelectedCollectionItems(action) {
  let ids = selectedCollectionIds();
  if (!ids.length) {
    await notify('请选择候选商品');
    return;
  }
  const text = action === 'skip' ? '跳过' : '删除';
  if (action === 'skip') {
    const importedIds = Array.from(document.querySelectorAll('[data-collection-id]:checked'))
      .filter(input => input.dataset.collectionStatus === 'imported')
      .map(input => Number(input.dataset.collectionId));
    if (importedIds.length) {
      ids = ids.filter(id => !importedIds.includes(id));
      if (!ids.length) {
        await notify('已入库的采集结果不能标记为跳过；如果只想清理采集结果，请使用批量删除。');
        return;
      }
    }
  }
  const hint = action === 'delete' ? '只会删除采集结果记录，不会删除商品库里的商品。' : '已入库商品不会被标记为跳过。';
  if (!await askConfirm(`确认${text}选中的 ${ids.length} 条候选商品吗？${hint}`)) return;
  const response = await fetch(`/api/collection-items/${action === 'skip' ? 'skip' : 'delete'}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || `${text}失败`);
    return;
  }
  await loadCollectionItems();
}

productsBody.addEventListener('click', async event => {
  const editId = event.target.dataset.edit;
  const deleteId = event.target.dataset.delete;
  const processImageId = event.target.dataset.processImage;
  const refreshImageId = event.target.dataset.refreshImage;
  if (editId) {
    openForm(products.find(product => product.id === Number(editId)));
  }
  if (processImageId) {
    await processProductImage(processImageId);
  }
  if (refreshImageId) {
    await refreshProductImage(refreshImageId);
  }
  if (deleteId && await askConfirm('确定删除这个商品吗？')) {
    await fetch(`/api/products/${deleteId}`, { method: 'DELETE' });
    await loadProducts();
  }
});

productsBody.addEventListener('change', async event => {
  const productId = event.target.dataset.image;
  const file = event.target.files?.[0];
  if (!productId || !file) return;
  const data = new FormData();
  data.append('image', file);
  await fetch(`/api/products/${productId}/image`, { method: 'POST', body: data });
  await loadProducts();
  await loadMissingImages();
});

async function processProductImage(productId, sourceImage = '') {
  const response = await fetch('/api/products/images/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), source_image: sourceImage }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '处理主图失败');
    return;
  }
  const result = await response.json();
  await notify(`${result.note}\n来源图：${result.source_image}\n任务ID：${result.task_id}\n状态：${result.status}\n稍后点击“查图”下载结果图。`);
}

async function refreshProductImage(productId) {
  const tasks = await fetchJson(`/api/products/${productId}/image-tasks`);
  if (!tasks.length) {
    await notify('这个商品还没有图生图任务，请先点“处理图”。');
    return;
  }
  const response = await fetch(`/api/image-tasks/${tasks[0].id}/refresh`, { method: 'POST' });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '查询图生图结果失败');
    return;
  }
  const result = await response.json();
  if (result.local_path) {
    openImagePreview(result.local_path, '处理后图片');
  }
  await notify(`${result.note}\n状态：${result.status}${result.local_path ? `\n本地图片：${result.local_path}` : ''}`);
}

promptForm?.addEventListener('submit', async event => {
  event.preventDefault();
  const payload = promptPayload();
  if (!payload.name) {
    await notify('请输入提示词名称');
    return;
  }
  const promptId = byId('promptId').value;
  const response = await fetch(promptId ? `/api/prompts/${promptId}` : '/api/prompts', {
    method: promptId ? 'PUT' : 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '保存提示词失败');
    return;
  }
  closePromptForm();
  await loadPrompts();
});

closePromptModal?.addEventListener('click', closePromptForm);
cancelPromptButton?.addEventListener('click', closePromptForm);

processingBody?.addEventListener('click', event => {
  const checkbox = event.target.closest('[data-processing-check]');
  if (checkbox) {
    event.stopPropagation();
    const productId = Number(checkbox.dataset.processingCheck);
    if (checkbox.checked) selectedProcessingIds.add(productId);
    else selectedProcessingIds.delete(productId);
    syncProcessingSelectAllState();
    return;
  }
  const deleteButton = event.target.closest('[data-processing-delete]');
  if (deleteButton) {
    event.preventDefault();
    event.stopPropagation();
    deleteProcessingProduct(deleteButton.dataset.processingDelete);
    return;
  }
  const selectButton = event.target.closest('[data-processing-select]');
  if (selectButton) {
    selectedProcessingProductId = Number(selectButton.dataset.processingSelect);
    renderProcessingItems();
    return;
  }
});

processingDetailPanel?.addEventListener('click', event => {
  const openPickerButton = event.target.closest('[data-open-slot-picker]');
  if (openPickerButton) {
    event.preventDefault();
    event.stopPropagation();
    const slot = openPickerButton.closest('[data-skc-drop-slot], [data-detail-drop-slot]');
    if (slot) openSlotImagePicker(slot);
    return;
  }
  const clearDetailSlot = event.target.closest('[data-clear-detail-slot]');
  if (clearDetailSlot) {
    event.preventDefault();
    event.stopPropagation();
    const slot = clearDetailSlot.closest('[data-detail-drop-slot]');
    if (slot) clearManualDetailImageAssignment(slot.dataset.productId, slot.dataset.slotIndex);
    return;
  }
  const clearSlot = event.target.closest('[data-clear-skc-slot]');
  if (clearSlot) {
    event.preventDefault();
    event.stopPropagation();
    const slot = clearSlot.closest('[data-skc-drop-slot]');
    if (slot) saveManualColorImageAssignment(slot.dataset.productId, slot.dataset.color, slot.dataset.slotIndex, '');
    return;
  }
  const imagePick = event.target.closest('[data-processing-image-pick]');
  if (imagePick) {
    event.preventDefault();
    event.stopPropagation();
    const productId = Number(imagePick.dataset.processingImagePick);
    const imageUrl = imagePick.dataset.imageUrl || '';
    if (!selectedProcessingImageUrls.has(productId)) selectedProcessingImageUrls.set(productId, new Set());
    const selectedUrls = selectedProcessingImageUrls.get(productId);
    if (selectedUrls.has(imageUrl)) selectedUrls.delete(imageUrl);
    else selectedUrls.add(imageUrl);
    if (!selectedUrls.size && imageUrl) selectedUrls.add(imageUrl);
    processingDetailPanel.querySelectorAll(`[data-processing-image-pick="${productId}"]`).forEach(card => {
      card.classList.toggle('active', selectedUrls.has(card.dataset.imageUrl || ''));
    });
    const sourceInput = document.querySelector(`[data-processing-image-source="${productId}"]`);
    if (sourceInput) sourceInput.value = Array.from(selectedUrls)[0] || '';
    const selectedBadge = processingDetailPanel.querySelector(`[data-selected-image-count="${productId}"]`);
    if (selectedBadge) selectedBadge.textContent = `已选 ${selectedUrls.size} 张`;
    return;
  }
  const autoAssignButton = event.target.closest('[data-auto-assign-images]');
  if (autoAssignButton) {
    autoAssignColorImages(autoAssignButton.dataset.autoAssignImages, autoAssignButton.dataset.count, autoAssignButton.dataset.useVision === 'true');
    return;
  }
});

processingDetailPanel?.addEventListener('dragstart', event => {
  const imageCard = event.target.closest('[data-draggable-image]');
  if (!imageCard) return;
  event.dataTransfer.effectAllowed = 'copy';
  event.dataTransfer.setData('text/plain', imageCard.dataset.imageUrl || '');
});

processingDetailPanel?.addEventListener('dragover', event => {
  const slot = event.target.closest('[data-skc-drop-slot], [data-detail-drop-slot]');
  if (!slot) return;
  event.preventDefault();
  slot.classList.add('drag-over');
  event.dataTransfer.dropEffect = 'copy';
});

processingDetailPanel?.addEventListener('dragleave', event => {
  const slot = event.target.closest('[data-skc-drop-slot], [data-detail-drop-slot]');
  if (slot) slot.classList.remove('drag-over');
});

processingDetailPanel?.addEventListener('drop', event => {
  const slot = event.target.closest('[data-skc-drop-slot], [data-detail-drop-slot]');
  if (!slot) return;
  event.preventDefault();
  slot.classList.remove('drag-over');
  const imageUrl = event.dataTransfer.getData('text/plain');
  if (!imageUrl) return;
  if (slot.dataset.detailDropSlot === 'true') saveManualDetailImageAssignment(slot.dataset.productId, slot.dataset.slotIndex, imageUrl);
  else saveManualColorImageAssignment(slot.dataset.productId, slot.dataset.color, slot.dataset.slotIndex, imageUrl);
});

async function deleteProcessingProduct(productId) {
  const item = processingItems.find(current => current.product_id === Number(productId));
  if (!await askConfirm(`确认删除商品 ${item?.skc || productId} 吗？商品库记录和对应主图都会删除。`)) return;
  const response = await fetch(`/api/products/${productId}`, { method: 'DELETE' });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '删除商品失败');
    return;
  }
  selectedProcessingIds.delete(Number(productId));
  selectedProcessingProductId = null;
  await refreshOperationalViews();
}

async function deleteSelectedProcessingProducts() {
  const ids = selectedProcessingProductIds();
  if (!ids.length) {
    await notify('请先勾选要删除的处理商品');
    return;
  }
  if (!await askConfirm(`确认删除选中的 ${ids.length} 个商品吗？商品库记录和对应主图都会删除。`)) return;
  const response = await fetch('/api/products/bulk/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '批量删除处理商品失败');
    return;
  }
  selectedProcessingIds.clear();
  selectedProcessingProductId = null;
  await refreshOperationalViews();
  await notify(`已删除 ${ids.length} 个商品`);
}

async function dedupeSelectedProcessingImages() {
  const ids = selectedProcessingProductIds();
  if (!ids.length) {
    await notify('请先勾选要图片去重的商品');
    return;
  }
  if (!await askConfirm(`确认对选中的 ${ids.length} 个商品执行图片去重吗？只会删除重复图片引用，不会物理删除原图文件。`)) return;
  const response = await fetch('/api/processing-items/dedupe-images', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '批量图片去重失败');
    return;
  }
  const result = await response.json();
  await loadProcessingItems();
  await notify(`图片去重完成：扫描 ${result.scanned_count || 0} 张，删除重复引用 ${result.removed_count || 0} 条（详情图 ${result.detail_removed_count || 0}，颜色图 ${result.color_removed_count || 0}）。`);
}

async function runProcessingBatchAction() {
  const action = processingBatchAction?.value || 'edit_fields';
  if (action === 'edit_fields') {
    openBatchProcessingForm();
    return;
  }
  if (action === 'generate_titles') {
    await batchGenerateProcessingTitles();
    return;
  }
  if (action === 'dedupe_images') {
    await dedupeSelectedProcessingImages();
    return;
  }
  if (action === 'delete') {
    await deleteSelectedProcessingProducts();
  }
}

processingDetailPanel?.addEventListener('change', event => {
  const productId = event.target.dataset.processingImageSource;
  if (!productId) return;
  const item = processingItems.find(current => current.product_id === Number(productId));
  const option = (item?.image_options || []).find(current => current.url === event.target.value);
  const preview = processingDetailPanel.querySelector('.image-picker-preview');
  if (preview && option) {
    preview.src = option.preview_url || option.url;
    preview.dataset.previewImage = option.preview_url || option.url;
  }
});

async function autoAssignColorImages(productId, count, useVision = false) {
  let userConfirmedVision = false;
  if (useVision) {
    userConfirmedVision = await askConfirm('识别分图会调用视觉 API，可能产生费用。确认现在执行图片识别吗？');
    if (!userConfirmedVision) return;
  }
  const response = await fetch('/api/processing-items/auto-assign-color-images', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), count_per_color: Number(count || 3), use_vision: useVision, user_confirmed_vision: userConfirmedVision }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '自动分图失败');
    return;
  }
  const result = await response.json();
  await notify(`自动分图完成：${result.assigned_count} 张，${Object.keys(result.colors || {}).length} 个颜色`);
  await loadProcessingItems();
}

async function detailImageAssignmentRequest(response, fallbackMessage) {
  if (!response.ok) {
    const text = await response.text();
    let message = fallbackMessage;
    try {
      const error = JSON.parse(text);
      message = error.detail || message;
    } catch (_error) {
      message = text || message;
    }
    await notify(message);
    return false;
  }
  await loadProcessingItems();
  return true;
}

async function saveManualDetailImageAssignment(productId, slotIndex, imageUrl) {
  const response = await fetch('/api/processing-items/detail-image-assignment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), slot_index: Number(slotIndex), image_url: imageUrl || '' }),
  });
  return detailImageAssignmentRequest(response, '保存详情图失败');
}

async function clearManualDetailImageAssignment(productId, slotIndex) {
  const response = await fetch(`/api/processing-items/${Number(productId)}/detail-images/${Number(slotIndex)}`, { method: 'DELETE' });
  if (response.status !== 404 && response.status !== 405) return detailImageAssignmentRequest(response, '删除详情图失败');
  const fallbackResponse = await fetch('/api/processing-items/detail-image-assignment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), slot_index: Number(slotIndex), image_url: '' }),
  });
  return detailImageAssignmentRequest(fallbackResponse, '删除详情图失败');
}

async function saveManualColorImageAssignment(productId, color, slotIndex, imageUrl) {
  const response = await fetch('/api/processing-items/color-image-assignment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), color, slot_index: Number(slotIndex), image_url: imageUrl || '' }),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '保存颜色图片失败');
    return;
  }
  await loadProcessingItems();
}

async function generateTitleForProduct(productId, options = {}) {
  const silent = Boolean(options.silent);
  addOperationLog('AI生成标题', 'running', `正在为商品 #${productId} 调用 DeepSeek 生成英文标题`, Math.max(operationProgress, 35));
  const response = await fetch('/api/processing-items/generate-title', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId) }),
  });
  if (!response.ok) {
    const error = await response.json();
    addOperationLog('AI生成标题', 'error', error.detail || '生成标题失败', operationProgress || 35);
    if (!silent) await notify(error.detail || '生成标题失败');
    throw new Error(error.detail || '生成标题失败');
  }
  const item = await response.json();
  if (!silent) {
    await loadProcessingItems();
    await notify(`已生成英文标题：
${item.english_title}`);
  }
  addOperationLog('AI生成标题', 'success', `已生成标题：${item.english_title}`, Math.max(operationProgress, 60));
  return item;
}

async function batchGenerateProcessingTitles() {
  const ids = selectedProcessingProductIds();
  if (!ids.length) {
    await notify('请先选择要处理标题的商品');
    return;
  }
  if (!await askConfirm(`确认批量处理 ${ids.length} 个商品标题吗？`)) return;
  let successCount = 0;
  let failedCount = 0;
  for (const productId of ids) {
    try {
      await generateTitleForProduct(productId, { silent: true });
      successCount += 1;
    } catch (error) {
      failedCount += 1;
    }
  }
  await loadProcessingItems();
  await notify(`批量标题处理完成：成功 ${successCount} 个，失败 ${failedCount} 个`);
}

processingForm?.addEventListener('submit', async event => {
  event.preventDefault();
  const payload = processingPayload();
  const productId = byId('processingProductId').value;
  const isBulk = processingFormMode === 'bulk';
  const startSkc = isBulk ? byId('processingSourceUrl').value.trim() : '';
  const response = await fetch(isBulk ? '/api/processing-items/bulk' : `/api/processing-items/${productId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(isBulk ? { ids: productId.split(',').map(Number), fields: payload, start_skc: startSkc } : payload),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '保存处理字段失败');
    return;
  }
  closeProcessingForm();
  await refreshOperationalViews();
  if (isBulk) await notify('批量字段保存完成');
});

productForm.addEventListener('submit', async event => {
  event.preventDefault();
  const productId = document.querySelector('#productId').value;
  const response = await fetch(productId ? `/api/products/${productId}` : '/api/products', {
    method: productId ? 'PUT' : 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formPayload()),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '保存失败');
    return;
  }
  closeForm();
  await loadProducts();
});

searchButton.addEventListener('click', loadProducts);
refreshButton.addEventListener('click', refreshOperationalViews);
if (batchImageInput) batchImageInput.addEventListener('change', batchUploadImages);
if (bulkProductStatusButton) bulkProductStatusButton.addEventListener('click', updateSelectedProductsStatus);
if (bulkProductDeleteButton) bulkProductDeleteButton.addEventListener('click', deleteSelectedProducts);
if (selectAllProducts) {
  selectAllProducts.addEventListener('change', () => {
    document.querySelectorAll('[data-product-select]').forEach(input => { input.checked = selectAllProducts.checked; });
  });
}
if (refreshProcessingButton) refreshProcessingButton.addEventListener('click', () => loadProcessingItems({ feedback: true }));
if (processingStatusFilter) processingStatusFilter.addEventListener('change', renderProcessingItems);
if (selectAllProcessing) selectAllProcessing.addEventListener('change', () => {
  const visibleIds = visibleProcessingItems().map(item => item.product_id);
  if (selectAllProcessing.checked) visibleIds.forEach(id => selectedProcessingIds.add(id));
  else visibleIds.forEach(id => selectedProcessingIds.delete(id));
  renderProcessingItems();
});
if (runProcessingBatchActionButton) runProcessingBatchActionButton.addEventListener('click', runProcessingBatchAction);
if (exportMiaoshouButton) exportMiaoshouButton.addEventListener('click', exportMiaoshou);
if (saveUploadOperationSettingsButton) saveUploadOperationSettingsButton.addEventListener('click', saveSettings);
if (createUploadTaskButton) createUploadTaskButton.addEventListener('click', realUpload);
if (createUploadTaskInlineButton) createUploadTaskInlineButton.addEventListener('click', createUploadTask);
if (clearUploadTasksButton) clearUploadTasksButton.addEventListener('click', clearUploadTasks);
if (preflightButton) preflightButton.addEventListener('click', runPreflight);
if (preflightInlineButton) preflightInlineButton.addEventListener('click', runPreflight);
if (realUploadButton) realUploadButton.addEventListener('click', realUpload);
if (realUploadInlineButton) realUploadInlineButton.addEventListener('click', realUpload);
if (clearOperationLogButton) clearOperationLogButton.addEventListener('click', () => {
  operationLogs = [];
  operationProgress = 0;
  renderOperationLogs();
});
if (refreshRecordsButton) refreshRecordsButton.addEventListener('click', loadPublishRecords);
if (retryFailedButton) retryFailedButton.addEventListener('click', realUpload);
recordsSearchInput?.addEventListener('keydown', event => { if (event.key === 'Enter') loadPublishRecords(); });
recordsResultFilter?.addEventListener('change', loadPublishRecords);
closeLogModal?.addEventListener('click', () => logModal.classList.add('hidden'));
uploadTasksBody?.addEventListener('click', event => {
  if (event.target.dataset.logTask) openTaskLog(event.target.dataset.logTask);
  if (event.target.dataset.deleteTask) deleteUploadTask(event.target.dataset.deleteTask);
});
if (saveApiButton) saveApiButton.addEventListener('click', saveApiConfigs);
if (saveSettingsButton) saveSettingsButton.addEventListener('click', saveSettings);
if (refreshSystemStatusButton) refreshSystemStatusButton.addEventListener('click', loadSystemStatus);
if (cleanupTestDataButton) cleanupTestDataButton.addEventListener('click', cleanupTestData);
if (newPromptButton) newPromptButton.addEventListener('click', createPrompt);
newProductButton.addEventListener('click', () => openForm());
closeModal.addEventListener('click', closeForm);
cancelButton.addEventListener('click', closeForm);
closeProcessingModal?.addEventListener('click', closeProcessingForm);
cancelProcessingButton?.addEventListener('click', closeProcessingForm);
searchInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') loadProducts();
});
productStatusFilter?.addEventListener('change', loadProducts);
productImageFilter?.addEventListener('change', loadProducts);
if (selectAllCollection) {
  selectAllCollection.addEventListener('change', () => {
    document.querySelectorAll('[data-collection-id]').forEach(input => {
      input.checked = selectAllCollection.checked;
    });
  });
}
byId('collectionSearchInput')?.addEventListener('keydown', event => { if (event.key === 'Enter') loadCollectionItems(); });
if (importSelectedButton) importSelectedButton.addEventListener('click', importSelectedCollectionItems);
if (deleteSelectedCollectionButton) deleteSelectedCollectionButton.addEventListener('click', () => updateSelectedCollectionItems('delete'));
if (applyCollectionFiltersButton) applyCollectionFiltersButton.addEventListener('click', loadCollectionItems);
if (startCollectionTaskButton) startCollectionTaskButton.addEventListener('click', startCollectionTask);
if (clearCollectionTasksButton) clearCollectionTasksButton.addEventListener('click', clearCollectionTasks);
if (collectionFileInput) collectionFileInput.addEventListener('change', importCollectionFile);
document.addEventListener('click', event => {
  if (event.target.closest('[data-processing-image-pick]')) return;
  const target = event.target.closest('[data-preview-image]');
  if (target) openImagePreview(target.dataset.previewImage, target.dataset.previewTitle);
});
document.addEventListener('mouseover', event => {
  const target = event.target.closest('[data-preview-image]');
  if (target) showHoverImagePreview(event, target);
});
document.addEventListener('mousemove', event => {
  if (hoverImagePreview && !hoverImagePreview.classList.contains('hidden')) positionHoverImagePreview(event);
});
document.addEventListener('mouseout', event => {
  const target = event.target.closest('[data-preview-image]');
  if (target && !target.contains(event.relatedTarget)) hideHoverImagePreview();
});
document.addEventListener('dragstart', hideHoverImagePreview);
collectionTasksBody?.addEventListener('click', event => {
  if (event.target.dataset.collectionRequest) openCollectionRequest(event.target.dataset.collectionRequest);
  if (event.target.dataset.collectionExecute) executeCollectionTask(event.target.dataset.collectionExecute);
  if (event.target.dataset.collectionResult) chooseCollectionResultFile(event.target.dataset.collectionResult);
});
closeCollectionRequestModal?.addEventListener('click', () => collectionRequestModal.classList.add('hidden'));
closeImagePreviewModal?.addEventListener('click', () => imagePreviewModal.classList.add('hidden'));
imagePreviewModal?.addEventListener('click', event => {
  if (event.target === imagePreviewModal) imagePreviewModal.classList.add('hidden');
});
closeSlotImagePickerModal?.addEventListener('click', closeSlotImagePicker);
cancelSlotImagePickerButton?.addEventListener('click', closeSlotImagePicker);
slotImagePickerModal?.addEventListener('click', event => {
  if (event.target === slotImagePickerModal) closeSlotImagePicker();
});
slotImagePickerGrid?.addEventListener('click', event => {
  const card = event.target.closest('[data-slot-picker-url]');
  if (card) toggleSlotPickerImage(card.dataset.slotPickerUrl);
});
confirmSlotImagePickerButton?.addEventListener('click', confirmSlotPickerImages);
if (collectionResultFileInput) collectionResultFileInput.addEventListener('change', importCollectionTaskResult);

refreshOperationalViews();
loadCollectionItems();
loadCollectionTasks();
loadApiConfigs();
loadSettings();
loadSystemStatus();
loadPrompts();
runPreflight();
