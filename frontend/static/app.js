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
const freightImportFile = document.querySelector('#freightImportFile');
const saveFreightRulesButton = document.querySelector('#saveFreightRulesButton');
const refreshFreightRulesButton = document.querySelector('#refreshFreightRulesButton');
const freightRuleSummary = document.querySelector('#freightRuleSummary');
const freightRuleDetails = document.querySelector('#freightRuleDetails');
const freightDefaultZone = document.querySelector('#freightDefaultZone');
const freightWarehouseFee = document.querySelector('#freightWarehouseFee');
const firstMileRuleEditor = document.querySelector('#firstMileRuleEditor');
const lastMileRuleEditor = document.querySelector('#lastMileRuleEditor');
const addFirstMileRuleButton = document.querySelector('#addFirstMileRuleButton');
const addLastMileRuleButton = document.querySelector('#addLastMileRuleButton');
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
const selectFilteredCollectionButton = document.querySelector('#selectFilteredCollectionButton');
const clearCollectionSelectionButton = document.querySelector('#clearCollectionSelectionButton');
const applyCollectionFiltersButton = document.querySelector('#applyCollectionFiltersButton');
const collectionPageInfo = document.querySelector('#collectionPageInfo');
const collectionPrevPageButton = document.querySelector('#collectionPrevPageButton');
const collectionNextPageButton = document.querySelector('#collectionNextPageButton');
const collectionPageSizeSelect = document.querySelector('#collectionPageSizeSelect');
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
let pendingCollectionResultTaskId = null;
let pendingSlotImagePick = null;
let pendingSlotImageUrls = new Set();
const processingBody = document.querySelector('#processingBody');
const processingDetailPanel = document.querySelector('#processingDetailPanel');
const processingDetailStatus = document.querySelector('#processingDetailStatus');
const processingStatusFilter = document.querySelector('#processingStatusFilter');
const processingSearchInput = document.querySelector('#processingSearchInput');
const processingExceptionTypeFilter = document.querySelector('#processingExceptionTypeFilter');
const processingListBadge = document.querySelector('#processingListBadge');
const processingPageInfo = document.querySelector('#processingPageInfo');
const processingPageSize = document.querySelector('#processingPageSize');
const processingTaskCenterBody = document.querySelector('#processingTaskCenterBody');
const processingTaskCenterBadge = document.querySelector('#processingTaskCenterBadge');
const processingTaskCenterPageInfo = document.querySelector('#processingTaskCenterPageInfo');
const processingTaskCenterPrev = document.querySelector('#processingTaskCenterPrev');
const processingTaskCenterNext = document.querySelector('#processingTaskCenterNext');
const processingTaskTypeFilter = document.querySelector('#processingTaskTypeFilter');
const processingTaskStatusFilter = document.querySelector('#processingTaskStatusFilter');
const refreshProcessingTasksButton = document.querySelector('#refreshProcessingTasksButton');
const processingPrevPage = document.querySelector('#processingPrevPage');
const processingNextPage = document.querySelector('#processingNextPage');
const selectAllProcessing = document.querySelector('#selectAllProcessing');
const processingBatchAction = document.querySelector('#processingBatchAction');
const processingFieldSettingsButton = document.querySelector('#processingFieldSettingsButton');
const processingFieldSettingsPanel = document.querySelector('#processingFieldSettingsPanel');
const saveProcessingFieldSettingsButton = document.querySelector('#saveProcessingFieldSettingsButton');
const processingSourceLabel = document.querySelector('#processingSourceLabel');
const refreshProcessingButton = document.querySelector('#refreshProcessingButton');
const processingModal = document.querySelector('#processingModal');
const processingForm = document.querySelector('#processingForm');
const closeProcessingModal = document.querySelector('#closeProcessingModal');
const cancelProcessingButton = document.querySelector('#cancelProcessingButton');
const createUploadTaskButton = document.querySelector('#createUploadTaskButton');
const createUploadTaskInlineButton = document.querySelector('#createUploadTaskInlineButton');
const saveUploadOperationSettingsButton = document.querySelector('#saveUploadOperationSettingsButton');
const clearUploadTasksButton = document.querySelector('#clearUploadTasksButton');
const cleanupLocalDataButton = document.querySelector('#cleanupLocalDataButton');
const preflightButton = document.querySelector('#preflightButton');
const refreshSpecMappingsButton = document.querySelector('#refreshSpecMappingsButton');
const specMappingSummary = document.querySelector('#specMappingSummary');
const specColorAliasBadge = document.querySelector('#specColorAliasBadge');
const specColorGroups = document.querySelector('#specColorGroups');
const specSizeChips = document.querySelector('#specSizeChips');
const specSizeAliasList = document.querySelector('#specSizeAliasList');
const specExceptionBadge = document.querySelector('#specExceptionBadge');
const specExceptionList = document.querySelector('#specExceptionList');
const specAliasKind = document.querySelector('#specAliasKind');
const specAliasInput = document.querySelector('#specAliasInput');
const specAliasTarget = document.querySelector('#specAliasTarget');
const saveSpecAliasButton = document.querySelector('#saveSpecAliasButton');
const specAliasSavedList = document.querySelector('#specAliasSavedList');
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
let selectedCollectionIdsSet = new Set();
let collectionPagination = { page: 1, page_size: 50, total: 0, total_pages: 1 };
let collectionTasks = [];
let processingItems = [];
let processingExceptionIds = new Set();
let processingExceptionMap = new Map();
let processingPreflightSummary = null;
let selectedProcessingProductId = null;
let selectedProcessingIds = new Set();
let selectedProcessingImageUrls = new Map();
let processingFormMode = 'single';
let processingPagination = { page: 1, page_size: 50, total: 0, total_pages: 1 };
let processingTasks = [];
let processingTaskCenter = { items: [], total: 0, page: 1, page_size: 20, total_pages: 1 };
let uploadTasks = [];
let publishRecords = [];
let specMappingsLoaded = false;
let specMappingColors = null;
let specMappingSizes = null;
let specAliasItems = [];
let specExceptionItems = [];
let missingImageProducts = [];
let operationLogs = [];
const FREIGHT_ZONES = ['zone1', 'zone2', 'zone3', 'zone4', 'zone5', 'zone6', 'zone7', 'zone8', 'zone9'];
let operationProgress = 0;
let collectionProgressLogs = [];
let collectionTaskEventsCache = new Map();
let collectionTaskPollingTimer = null;
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
    collectionProgressBody.innerHTML = '<div class="chat-empty">\u6682\u65e0\u91c7\u96c6\u65e5\u5fd7</div>';
    return;
  }
  collectionProgressBody.innerHTML = collectionProgressLogs.slice(0, 50).map(log => `
    <div class="chat-row ${log.type}">
      <div class="chat-avatar">${log.type === 'success' ? '?' : (log.type === 'error' ? '!' : '?')}</div>
      <div class="chat-bubble">
        <div class="chat-meta"><b>${log.step}</b><span>${log.time}</span><em class="log-status ${log.type}">${log.statusText}</em></div>
        <div class="chat-message">${log.message}</div>
      </div>
    </div>
  `).join('');
}

function addCollectionProgressLog(step, type = 'info', message = '') {
  const statusMap = { running: '\u5904\u7406\u4e2d', success: '\u5b8c\u6210', error: '\u9700\u5904\u7406', info: '\u8bb0\u5f55' };
  collectionProgressLogs.unshift({ time: new Date().toLocaleTimeString(), step, type, statusText: statusMap[type] || statusMap.info, message });
  renderCollectionProgressLogs();
}


function openProgressDialog({ title = '执行进度', message = '正在处理，请稍候...', okText = '关闭' } = {}) {
  if (!appDialogModal) return;
  appDialogTitle.textContent = title;
  appDialogMessage.innerHTML = `<div id="appDialogProgressText" class="app-dialog-progress-text">${message}</div>`;
  appDialogOk.textContent = okText;
  appDialogOk.style.display = 'none';
  appDialogCancel.style.display = 'none';
  appDialogOk.onclick = () => appDialogModal.classList.add('hidden');
  appDialogClose.onclick = () => appDialogModal.classList.add('hidden');
  appDialogModal.classList.remove('hidden');
}

function updateProgressDialogText(message, done = false) {
  const target = document.querySelector('#appDialogProgressText');
  if (!target) return;
  target.textContent = message;
  appDialogOk.style.display = done ? '' : 'none';
  appDialogOk.textContent = done ? '完成' : appDialogOk.textContent;
}

function pushDialogProgress(logs, step, type, message) {
  logs.unshift({ time: new Date().toLocaleTimeString(), step, type, message });
  updateProgressDialogText(message, type === 'success' || type === 'error');
  addCollectionProgressLog(step, type, message);
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

function fillProcessingFieldSettingsForm() {
  if (byId('defaultProcessingDeclaredPriceMode')) byId('defaultProcessingDeclaredPriceMode').value = settingValue('default_processing_declared_price_mode') || 'add';
  if (byId('defaultProcessingDeclaredPrice')) byId('defaultProcessingDeclaredPrice').value = settingValue('default_processing_declared_price') || '0';
  if (byId('defaultProcessingWeightG')) byId('defaultProcessingWeightG').value = settingValue('default_processing_weight_g') || '350';
  if (byId('defaultProcessingLengthCm')) byId('defaultProcessingLengthCm').value = settingValue('default_processing_length_cm') || '15';
  if (byId('defaultProcessingWidthCm')) byId('defaultProcessingWidthCm').value = settingValue('default_processing_width_cm') || '10';
  if (byId('defaultProcessingHeightCm')) byId('defaultProcessingHeightCm').value = settingValue('default_processing_height_cm') || '2';
  if (byId('defaultProcessingStock')) byId('defaultProcessingStock').value = settingValue('default_processing_stock') || '999';
  if (byId('defaultProcessingShipDays')) byId('defaultProcessingShipDays').value = settingValue('default_processing_ship_days') || '9';
  if (byId('defaultProcessingStartSkc')) byId('defaultProcessingStartSkc').value = settingValue('default_processing_start_skc') || '';
}

function defaultProcessingFieldsPayload() {
  return {
    english_title: '',
    color: '',
    size: '',
    sku_code: '',
    declared_price: Number(byId('defaultProcessingDeclaredPrice')?.value || 0),
    declared_price_mode: byId('defaultProcessingDeclaredPriceMode')?.value || 'add',
    weight_g: Number(byId('defaultProcessingWeightG')?.value || 350),
    length_cm: Number(byId('defaultProcessingLengthCm')?.value || 15),
    width_cm: Number(byId('defaultProcessingWidthCm')?.value || 10),
    height_cm: Number(byId('defaultProcessingHeightCm')?.value || 2),
    source_url: '',
    stock: Number(byId('defaultProcessingStock')?.value || 999),
    ship_days: Number(byId('defaultProcessingShipDays')?.value || 9),
  };
}

function fillSettingsForm() {
  fillProcessingFieldSettingsForm();
  if (byId('settingRunMode')) byId('settingRunMode').value = settingValue('run_mode') || 'headless';
  if (byId('settingMaxRetries')) byId('settingMaxRetries').value = settingValue('max_retries') || '2';
  if (byId('settingAiTitleRequestDelaySeconds')) byId('settingAiTitleRequestDelaySeconds').value = settingValue('ai_title_request_delay_seconds') || '0.35';
  if (byId('settingAiTitleMaxRetries')) byId('settingAiTitleMaxRetries').value = settingValue('ai_title_max_retries') || '1';
  if (byId('settingAiTitleRetryDelaySeconds')) byId('settingAiTitleRetryDelaySeconds').value = settingValue('ai_title_retry_delay_seconds') || '2';
  if (byId('settingAiTitleWorkerConcurrency')) byId('settingAiTitleWorkerConcurrency').value = settingValue('ai_title_worker_concurrency') || '1';

  if (byId('settingUploadImageSource')) byId('settingUploadImageSource').value = settingValue('upload_image_source') || '';
  if (byId('settingCosRegion')) byId('settingCosRegion').value = settingValue('cos_region') || '';
  if (byId('settingCosBucket')) byId('settingCosBucket').value = settingValue('cos_bucket') || '';
  if (byId('settingCosPrefix')) byId('settingCosPrefix').value = settingValue('cos_prefix') || '';
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

const DEFAULT_PROMPT_KEYS = new Set([
  'Temu 英文标题生成|女装短裤|标题提示词|标题生成',
  '服饰中英文标题生成|服饰通用|标题提示词|标题生成',
  '牛仔短裤主图精修|女装短裤|图生图提示词|主图优化',
  '商品颜色图片识别|通用商品|图片识别提示词|颜色分图',
]);

function promptTemplateKey(prompt) {
  return [prompt?.name || '', prompt?.category || '', prompt?.prompt_type || '', prompt?.usage || ''].join('|');
}

function isDefaultPrompt(prompt) {
  return DEFAULT_PROMPT_KEYS.has(promptTemplateKey(prompt));
}

function renderPrompts() {
  if (!promptsBody) return;
  if (!prompts.length) {
    promptsBody.innerHTML = '<tr><td class="empty-row" colspan="6">暂无提示词模板</td></tr>';
    return;
  }
  promptsBody.innerHTML = prompts.map(prompt => {
    const deleteButton = isDefaultPrompt(prompt)
      ? '<span class="muted">默认提示词不可删除</span>'
      : `<button class="btn outline-orange" data-prompt-delete="${prompt.id}">删除</button>`;
    return `
    <tr>
      <td>${prompt.name}</td>
      <td>${prompt.category}</td>
      <td>${prompt.prompt_type}</td>
      <td>${prompt.usage}</td>
      <td><span class="badge ${prompt.status === '启用中' ? 'green' : 'orange'}">${prompt.status}</span></td>
      <td><button class="btn ghost" data-prompt-edit="${prompt.id}">编辑</button>${deleteButton}</td>
    </tr>
  `;
  }).join('');
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
    { key: 'ai_title_request_delay_seconds', value: byId('settingAiTitleRequestDelaySeconds')?.value || '0.35' },
    { key: 'ai_title_max_retries', value: byId('settingAiTitleMaxRetries')?.value || '1' },
    { key: 'ai_title_retry_delay_seconds', value: byId('settingAiTitleRetryDelaySeconds')?.value || '2' },
    { key: 'ai_title_worker_concurrency', value: byId('settingAiTitleWorkerConcurrency')?.value || '1' },
    { key: 'default_processing_declared_price_mode', value: byId('defaultProcessingDeclaredPriceMode')?.value || 'add' },
    { key: 'default_processing_declared_price', value: byId('defaultProcessingDeclaredPrice')?.value || '0' },
    { key: 'default_processing_weight_g', value: byId('defaultProcessingWeightG')?.value || '350' },
    { key: 'default_processing_length_cm', value: byId('defaultProcessingLengthCm')?.value || '15' },
    { key: 'default_processing_width_cm', value: byId('defaultProcessingWidthCm')?.value || '10' },
    { key: 'default_processing_height_cm', value: byId('defaultProcessingHeightCm')?.value || '2' },
    { key: 'default_processing_stock', value: byId('defaultProcessingStock')?.value || '999' },
    { key: 'default_processing_ship_days', value: byId('defaultProcessingShipDays')?.value || '9' },
    { key: 'default_processing_start_skc', value: byId('defaultProcessingStartSkc')?.value || '' },
    { key: 'upload_image_source', value: byId('settingUploadImageSource')?.value || '' },
    { key: 'cos_region', value: byId('settingCosRegion')?.value || '' },
    { key: 'cos_bucket', value: byId('settingCosBucket')?.value || '' },
    { key: 'cos_prefix', value: byId('settingCosPrefix')?.value || '' },
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
      <div><b>真实 RPA：</b><span class="badge green">点击开始上货直接执行</span></div>
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
loadFreightRules();
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
    const response = await fetch(`/api/prompts/${deleteId}`, { method: 'DELETE' });
    if (!response.ok) {
      const error = await response.json();
      await notify(error.detail || '删除提示词失败');
      return;
    }
    await loadPrompts();
  }
});


navItems.forEach(item => {
  item.addEventListener('click', () => {
    navItems.forEach(nav => nav.classList.remove('active'));
    pages.forEach(page => page.classList.remove('active-page'));
    item.classList.add('active');
    document.querySelector(`#${item.dataset.page}`)?.classList.add('active-page');
    if (item.dataset.page === 'spec-mapping') loadSpecMappings();
    if (item.dataset.page === 'processing-tasks') loadProcessingTaskCenter({ page: 1 });
    if (item.dataset.page === 'profit-management') loadFreightRules();
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

function renderSpecMappingSummary(colors, sizes) {
  if (!specMappingSummary) return;
  const groups = colors.groups || [];
  const standardColors = colors.standard_colors || [];
  const standardSizes = sizes.sizes || [];
  specMappingSummary.innerHTML = `
    <div class="metric-card"><span>颜色色系</span><b>${groups.length}</b><em>来自平台标准表</em></div>
    <div class="metric-card"><span>标准颜色</span><b>${standardColors.length}</b><em>供应商颜色归一目标</em></div>
    <div class="metric-card"><span>颜色别名</span><b>${colors.alias_count || 0}</b><em>含英文与常见简称</em></div>
    <div class="metric-card"><span>标准尺码</span><b>${standardSizes.length}</b><em>${sizes.name || '当前类目'}</em></div>
  `;
}

function renderSpecColorGroups(data) {
  if (!specColorGroups) return;
  const groups = data.groups || [];
  if (!groups.length) {
    specColorGroups.innerHTML = '<div class="empty-row">暂无颜色标准表</div>';
    return;
  }
  specColorGroups.innerHTML = groups.map(group => `
    <div class="spec-map-group">
      <div class="spec-map-group-title"><b>${group.name}</b><span>${(group.colors || []).length} 个</span></div>
      <div class="spec-chip-list">${(group.colors || []).map(color => `<span class="spec-chip">${color}</span>`).join('')}</div>
    </div>
  `).join('');
  if (specColorAliasBadge) specColorAliasBadge.textContent = `${data.alias_count || 0} 个别名`;
}

function renderSpecSizes(data) {
  if (specSizeChips) {
    const sizes = sortUploadSizes(data.sizes || []);
    specSizeChips.innerHTML = sizes.length ? sizes.map(size => `<span class="size-chip supported">${size}</span>`).join('') : '<div class="empty-row">暂无尺码标准表</div>';
  }
  if (specSizeAliasList) {
    const aliasMap = data.alias_map || {};
    const aliases = Object.entries(aliasMap).filter(([alias, size]) => alias !== size);
    specSizeAliasList.innerHTML = aliases.length ? `
      <div class="spec-alias-title">尺码别名归一</div>
      ${aliases.map(([alias, size]) => `<span><b>${alias}</b> → ${size}</span>`).join('')}
    ` : '<div class="desc">暂无额外尺码别名</div>';
  }
}

function renderSpecAliasTargets() {
  if (!specAliasTarget) return;
  const kind = specAliasKind?.value || 'color';
  const options = kind === 'size' ? sortUploadSizes(specMappingSizes?.sizes || []) : (specMappingColors?.standard_colors || []);
  specAliasTarget.innerHTML = options.map(option => `<option value="${option}">${option}</option>`).join('');
}

function renderSpecAliasSavedList() {
  if (!specAliasSavedList) return;
  if (!specAliasItems.length) {
    specAliasSavedList.innerHTML = '<div class="empty-row">暂无自定义绑定</div>';
    return;
  }
  specAliasSavedList.innerHTML = `
    <div class="spec-alias-title">已保存绑定</div>
    ${specAliasItems.map(item => `<span><b>${item.kind === 'color' ? '颜色' : '尺码'} · ${item.alias}</b> → ${item.target}<button class="spec-alias-delete" data-spec-alias-delete="${item.id}" type="button" title="删除绑定">×</button></span>`).join('')}
  `;
}

function specTargetOptions(kind) {
  const options = kind === 'size' ? sortUploadSizes(specMappingSizes?.sizes || []) : (specMappingColors?.standard_colors || []);
  return options.map(option => `<option value="${option}">${option}</option>`).join('');
}

function renderSpecExceptions() {
  if (specExceptionBadge) specExceptionBadge.textContent = `${specExceptionItems.length} 个`;
  if (!specExceptionList) return;
  if (!specExceptionItems.length) {
    specExceptionList.innerHTML = '<div class="empty-row">暂无待修复规格异常</div>';
    return;
  }
  specExceptionList.innerHTML = specExceptionItems.map((item, index) => `
    <div class="spec-exception-row">
      <div><b>${item.kind === 'color' ? '颜色' : '尺码'}：${item.value}</b><span>影响 ${item.count} 个商品</span></div>
      <select class="select" data-spec-exception-target="${index}">${specTargetOptions(item.kind)}</select>
      <button class="btn primary" data-spec-exception-bind="${index}" type="button">批量绑定</button>
    </div>
  `).join('');
}

async function saveSpecAliasPayload(kind, alias, target) {
  return fetchJson('/api/spec-mappings/aliases', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ kind, alias, target }),
  });
}

async function bindSpecException(index) {
  const item = specExceptionItems[Number(index)];
  if (!item) return;
  const targetSelect = specExceptionList?.querySelector(`[data-spec-exception-target="${index}"]`);
  const target = targetSelect?.value || '';
  if (!target) {
    await showAlert('请选择要绑定的标准值');
    return;
  }
  await saveSpecAliasPayload(item.kind, item.value, target);
  specMappingsLoaded = false;
  await loadSpecMappings(true);
  await loadProcessingItems();
}

async function deleteSpecAlias(aliasId) {
  if (!aliasId) return;
  if (!await askConfirm('确认删除这个规格绑定吗？删除后后续商品会重新进入异常池。')) return;
  await fetchJson(`/api/spec-mappings/aliases/${aliasId}`, { method: 'DELETE' });
  specMappingsLoaded = false;
  await loadSpecMappings(true);
  await loadProcessingItems();
}

async function saveSpecAlias() {
  const kind = specAliasKind?.value || 'color';
  const alias = specAliasInput?.value.trim() || '';
  const target = specAliasTarget?.value || '';
  if (!alias || !target) {
    await showAlert('请填写供应商写法并选择标准值');
    return;
  }
  await saveSpecAliasPayload(kind, alias, target);
  if (specAliasInput) specAliasInput.value = '';
  specMappingsLoaded = false;
  await loadSpecMappings(true);
  await loadProcessingItems();
}

async function loadSpecMappings(force = false) {
  if (!force && specMappingsLoaded) return;
  if (specColorGroups) specColorGroups.innerHTML = '<div class="empty-row">正在加载颜色映射...</div>';
  if (specSizeChips) specSizeChips.innerHTML = '<div class="empty-row">正在加载尺码映射...</div>';
  try {
    const [colors, sizes, aliases, exceptions] = await Promise.all([
      fetchJson('/api/spec-mappings/colors'),
      fetchJson('/api/spec-mappings/sizes'),
      fetchJson('/api/spec-mappings/aliases'),
      fetchJson('/api/spec-mappings/exceptions'),
    ]);
    specMappingColors = colors;
    specMappingSizes = sizes;
    specAliasItems = aliases || [];
    specExceptionItems = exceptions || [];
    renderSpecMappingSummary(colors, sizes);
    renderSpecColorGroups(colors);
    renderSpecSizes(sizes);
    renderSpecAliasTargets();
    renderSpecAliasSavedList();
    renderSpecExceptions();
    specMappingsLoaded = true;
  } catch (error) {
    if (specColorGroups) specColorGroups.innerHTML = `<div class="empty-row">加载失败：${error.message}</div>`;
    if (specSizeChips) specSizeChips.innerHTML = '<div class="empty-row">加载失败</div>';
  }
}

function collectionStatusText(status) {
  const map = {
    pending: '\u5f85\u786e\u8ba4',
    imported: '\u5df2\u52a0\u5165\u5546\u54c1\u5e93',
    skipped: '\u5df2\u8df3\u8fc7',
    queued: '\u6392\u961f\u4e2d',
    running: '\u8fd0\u884c\u4e2d',
    cancel_requested: '\u53d6\u6d88\u4e2d',
    cancelled: '\u5df2\u53d6\u6d88',
    completed: '\u5df2\u5b8c\u6210',
    empty: '\u65e0\u7ed3\u679c',
    external_pending: '\u5f85\u4eba\u5de5\u786e\u8ba4',
    blocked: '\u5df2\u963b\u65ad',
    failed: '\u5931\u8d25',
  };
  return map[status] || status;
}


function collectionTaskStatusClass(status) {
  if (status === 'completed') return 'green';
  if (status === 'failed') return 'red';
  if (status === 'queued' || status === 'empty' || status === 'external_pending' || status === 'blocked' || status === 'cancel_requested' || status === 'cancelled') return 'orange';
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
    queued_for_executor: '等待本机上货',
    claimed_by_executor: '本机执行中',
    rpa_success: 'RPA 成功',
    rpa_failed: 'RPA 失败',
  };
  return map[status] || status;
}

function displayTaskNote(note) {
  return String(note || '').replace(/\s*;?\s*imported_product_ids=[\d,\s]+/g, '').trim();
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
  const colors = uniqueList([...matrix.colors.map(entry => entry.color).filter(Boolean), ...Array.from(assignmentsByColor.keys())]);
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

function collectionEventStageText(stage) {
  const map = {
    queued: '\u6392\u961f',
    created: '\u521b\u5efa\u4efb\u52a1',
    parsed: '\u89e3\u6790\u7ed3\u679c',
    execute: '\u6267\u884c\u91c7\u96c6',
    background_start: '\u540e\u53f0\u542f\u52a8',
    write: '\u5199\u5165\u7ed3\u679c',
    finished: '\u4efb\u52a1\u5b8c\u6210',
    error: '\u9519\u8bef',
    import_result: '\u56de\u586b\u7ed3\u679c',
    resume: '\u6062\u590d\u961f\u5217',
  };
  return map[stage] || stage;
}

function collectionEventStatusText(status) {
  const map = {
    running: '\u5904\u7406\u4e2d',
    success: '\u5b8c\u6210',
    error: '\u5931\u8d25',
    info: '\u8bb0\u5f55',
  };
  return map[status] || status;
}

function cleanLogText(value) {
  let text = String(value || '').replace(/\?{3,}/g, '[old garbled log]');
  text = text.replace(/task re-queued/gi, '\u4efb\u52a1\u5df2\u91cd\u65b0\u52a0\u5165\u91c7\u96c6\u961f\u5217');
  text = text.replace(/task queued/gi, '\u4efb\u52a1\u5df2\u52a0\u5165\u91c7\u96c6\u961f\u5217');
  text = text.replace(/task started/gi, '\u91c7\u96c6\u4efb\u52a1\u5f00\u59cb\u6267\u884c');
  text = text.replace(/start provider=(.*?), target=(\d+)/gi, '\u5f00\u59cb\u91c7\u96c6\uff1a\u6765\u6e90=$1\uff0c\u76ee\u6807=$2 \u6761');
  text = text.replace(/parsed (\d+), imported (\d+), skipped (\d+)/gi, '\u89e3\u6790 $1 \u6761\uff0c\u65b0\u589e $2 \u6761\uff0c\u8df3\u8fc7 $3 \u6761');
  return text;
}


async function openCollectionTaskEvents(taskId) {
  const events = await fetchJson(`/api/collection-tasks/${taskId}/events`);
  collectionTaskEventsCache.set(Number(taskId), events || []);
  const task = collectionTasks.find(item => item.id === Number(taskId));
  const lines = [];
  if (task) {
    lines.push(`???? #${task.id} ${task.keyword}`);
    lines.push(`???${collectionStatusText(task.status)} | ???${task.target_count} | ???${task.result_count || 0}`);
    lines.push(`???${cleanLogText(task.note || '-')}`);
    lines.push('');
  }
  if (!events.length) {
    lines.push('?????????');
  } else {
    events.forEach(event => {
      const counts = [`??=${event.parsed_count || 0}`, `??=${event.imported_count || 0}`, `??=${event.skipped_count || 0}`].join(' ');
      lines.push(`[${event.created_at}] ${collectionEventStatusText(event.status)} ? ${collectionEventStageText(event.stage)}${event.page_no ? ` ?${event.page_no}?` : ''} ? ${counts}`);
      if (event.message) lines.push(`  ${cleanLogText(event.message)}`);
    });
  }
  logContent.textContent = lines.join('\n');
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

async function retryFailedUpload() {
  if (!await askConfirm('确认只重试当前失败记录对应的商品吗？成功/排队记录不会重复提交。')) return;
  addOperationLog('失败重试', 'running', '正在生成失败商品重试任务', Math.max(operationProgress, 35));
  const response = await fetch('/api/upload-tasks/retry-failed', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids: [] }),
  });
  if (!response.ok) {
    const error = await response.json();
    addOperationLog('失败重试', 'error', error.detail || '失败重试任务创建失败', operationProgress || 35);
    await notify(error.detail || '失败重试任务创建失败');
    return;
  }
  const task = await response.json();
  await refreshOperationalViews();
  addOperationLog('失败重试', 'success', `已创建重试任务 #${task.id}，状态：${taskStatusText(task.status)}`, 75);
  await notify(`已创建失败重试任务。\n任务：${task.name}\n商品数：${task.total_count}\n状态：${taskStatusText(task.status)}`);
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





function requiredTemuUploadSettings() {
  return [
    { id: 'settingTemuShopAccount', label: '店铺账号' },
    { id: 'settingTemuSite', label: '经营站点' },
    { id: 'settingTemuProductTemplate', label: '产品模板' },
    { id: 'settingTemuSizeCategory', label: '尺码分类' },
    { id: 'settingTemuSizeTemplate', label: '尺码模板' },
    { id: 'settingTemuWarehouseTemplate', label: '仓库模板' },
    { id: 'settingTemuLogisticsTemplate', label: '物流模板' },
  ];
}

async function validateTemuUploadSettings() {
  const missing = requiredTemuUploadSettings().filter(item => !byId(item.id)?.value.trim());
  if (!missing.length) return true;
  await notify(`请先填写店铺与模板必填项：\n${missing.map(item => `- ${item.label}`).join('\n')}`, '上货配置未填写完整');
  byId(missing[0].id)?.focus();
  return false;
}

async function realUpload() {
  if (!await validateTemuUploadSettings()) return;
  await saveSettings({ silent: true });
  addOperationLog('开始上货', 'running', '正在开始上货', 62);
  const response = await fetch('/api/upload-tasks/run', { method: 'POST' });
  const task = await response.json();
  await refreshOperationalViews();
  const queued = task.status === 'queued_for_executor' || task.status === 'claimed_by_executor';
  addOperationLog('开始上货', task.status === 'rpa_success' ? 'success' : (task.status === 'blocked' || task.status === 'needs_review' || task.status === 'rpa_failed' ? 'error' : 'info'), task.run_log || `任务状态：${task.status}`, task.status === 'rpa_success' ? 100 : (queued ? 82 : 72));
  await notify(task.run_log || '开始上货已执行');
}

async function createUploadTask() {
  if (!await validateTemuUploadSettings()) return;
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

async function cleanupLocalData() {
  if (!await askConfirm('确认清理 7 天前的成功任务、旧导出和旧日志吗？失败商品和失败记录不会自动清理。')) return;
  const result = await fetchJson('/api/local/cleanup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ retention_days: 7, clean_success_images: true, clean_exports: true, clean_logs: true }),
  });
  await refreshOperationalViews();
  await notify(`清理完成：导出 ${result.deleted_exports}，日志 ${result.deleted_logs}，成功商品图片 ${result.deleted_success_images}，成功任务 ${result.deleted_upload_tasks}`);
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

function renderCollectionPagination() {
  if (!collectionPageInfo) return;
  const page = collectionPagination.page || 1;
  const totalPages = collectionPagination.total_pages || 1;
  const total = collectionPagination.total || 0;
  const pageSize = collectionPagination.page_size || 50;
  const startIndex = total ? ((page - 1) * pageSize + 1) : 0;
  const endIndex = total ? Math.min(page * pageSize, total) : 0;
  collectionPageInfo.textContent = `\u7b2c ${page} / ${totalPages} \u9875\uff0c\u5171 ${total} \u6761\uff0c\u5f53\u524d ${startIndex}-${endIndex}`;
  if (collectionPrevPageButton) collectionPrevPageButton.disabled = page <= 1;
  if (collectionNextPageButton) collectionNextPageButton.disabled = page >= totalPages;
  if (collectionPageSizeSelect) collectionPageSizeSelect.value = String(pageSize);
  updateCollectionSelectionSummary();
}


function syncCollectionSelectAllState() {
  if (!selectAllCollection) return;
  const pageIds = collectionItems.map(item => item.id);
  const checkedCount = pageIds.filter(id => selectedCollectionIdsSet.has(id)).length;
  selectAllCollection.checked = Boolean(pageIds.length && checkedCount === pageIds.length);
  selectAllCollection.indeterminate = Boolean(checkedCount && checkedCount < pageIds.length);
}

function updateCollectionSelectionSummary() {
  if (!collectionPageInfo) return;
  const selectedCount = selectedCollectionIdsSet.size;
  if (!selectedCount) return;
  collectionPageInfo.textContent += `\uff0c\u5df2\u9009 ${selectedCount} \u6761`;
}

function renderCollectionItems() {
  if (!collectionBody) return;
  if (!collectionItems.length) {
    collectionBody.innerHTML = '<tr><td class="empty-row" colspan="8">\u6682\u65e0\u91c7\u96c6\u7ed3\u679c\uff0c\u8bf7\u5f00\u59cb\u771f\u5b9e\u91c7\u96c6\u6216\u5bfc\u5165 CSV/XLSX/JSON</td></tr>';
    renderCollectionPagination();
    return;
  }
  collectionBody.innerHTML = collectionItems.map(item => `
    <tr>
      <td><input type="checkbox" data-collection-id="${item.id}" data-collection-status="${item.status}" ${selectedCollectionIdsSet.has(item.id) ? 'checked' : ''}></td>
      <td>${item.image_url ? `<img class="thumb collection-thumb" src="${item.image_url}" alt="${item.title}" loading="lazy" referrerpolicy="no-referrer" data-preview-image="${item.image_url}" data-preview-title="${item.title}" onerror="this.onerror=null;this.src='/api/image-proxy?url=${encodeURIComponent(item.image_url)}';">` : '<span class="desc">\u65e0\u56fe</span>'}</td>
      <td>${item.source_url ? `<a href="${item.source_url}" target="_blank" rel="noopener">${item.title}</a>` : item.title}</td>
      <td>${item.source}</td>
      <td>${money(item.price)}</td>
      <td>${item.sales}</td>
      <td>${item.image_count} \u5f20</td>
      <td><span class="badge ${item.status === 'imported' ? 'green' : 'orange'}">${collectionStatusText(item.status)}</span></td>
    </tr>
  `).join('');
  renderCollectionPagination();
  syncCollectionSelectAllState();
}




function processingExceptionType(item) {
  const exception = processingExceptionMap.get(item.product_id);
  const lines = exception ? [...(exception.issues || []), ...(exception.warnings || [])] : [];
  if (!lines.length) return '';
  if (lines.some(line => /标题|SKU Code/.test(line))) return 'title';
  if (lines.some(line => /颜色|尺码|标准色/.test(line))) return 'spec';
  if (lines.some(line => /主图|颜色图|图片/.test(line))) return 'image';
  if (lines.some(line => /申报价|重量|尺寸|库存|发货/.test(line))) return 'field';
  if (lines.some(line => /链接/.test(line))) return 'link';
  return 'other';
}

function filteredProcessingItems() {
  const statusFilter = processingStatusFilter?.value || '';
  const keyword = String(processingSearchInput?.value || '').trim().toLowerCase();
  const exceptionType = processingExceptionTypeFilter?.value || '';
  let items = processingItems;
  if (keyword) {
    items = items.filter(item => [item.skc, item.title, item.english_title, item.source_url, item.color, item.size, item.sku_code].some(value => String(value || '').toLowerCase().includes(keyword)));
  }
  if (statusFilter === 'exception_pool') items = items.filter(item => processingExceptionIds.has(item.product_id));
  else if (statusFilter === 'ready_to_export') items = items.filter(item => processingColorReadiness(item).ready);
  else if (statusFilter === 'needs_image') items = items.filter(item => !processingColorReadiness(item).ready);
  else if (statusFilter) items = items.filter(item => item.status === statusFilter);
  if (exceptionType) items = items.filter(item => processingExceptionType(item) === exceptionType);
  return items;
}

function visibleProcessingItems() {
  return filteredProcessingItems();
}

function pagedProcessingItems() {
  return filteredProcessingItems();
}

function selectedProcessingProductIds() {
  const checkedIds = Array.from(document.querySelectorAll('[data-processing-check]:checked')).map(input => Number(input.dataset.processingCheck));
  const mergedIds = new Set([...selectedProcessingIds, ...checkedIds]);
  return Array.from(mergedIds).filter(id => processingItems.some(item => item.product_id === id));
}

function syncProcessingSelectAllState() {
  if (!selectAllProcessing) return;
  const visibleItems = pagedProcessingItems();
  const visibleIds = visibleItems.map(item => item.product_id);
  const checkedCount = visibleIds.filter(id => selectedProcessingIds.has(id)).length;
  selectAllProcessing.checked = Boolean(visibleIds.length && checkedCount === visibleIds.length);
  selectAllProcessing.indeterminate = Boolean(checkedCount && checkedCount < visibleIds.length);
}

function processingTaskStatusText(status) {
  const map = {
    queued: '排队中',
    running: '运行中',
    completed: '已完成',
    failed: '失败',
  };
  return map[status] || status || '未知';
}

function processingTaskStatusClass(status) {
  if (status === 'completed') return 'green';
  if (status === 'failed') return 'red';
  if (status === 'running') return 'blue';
  return 'orange';
}

function processingTaskRowsHtml(tasks) {
  if (!tasks.length) return '<div class="empty-row">暂无处理任务</div>';
  return tasks.map(task => {
    const percent = task.total_count ? Math.round((task.processed_count || 0) / task.total_count * 100) : 0;
    const cacheText = task.cache_hit_count ? ` · 缓存 ${task.cache_hit_count}` : '';
    const retryButton = task.retryable_count ? `<button class="btn ghost" data-processing-task-retry="${task.task_type}:${task.id}" type="button">重试失败 ${task.retryable_count}</button>` : '';
    return `
      <div class="processing-task-row">
        <div class="processing-task-main"><b>${task.task_label} #${task.id}</b><span>${displayTaskNote(task.note) || '暂无备注'}</span></div>
        <div class="processing-task-progress"><span>${task.processed_count || 0}/${task.total_count || 0} · 成功 ${task.success_count || 0} · 失败 ${task.failed_count || 0}${cacheText}</span><div class="progress-track mini"><div class="progress-bar" style="width:${percent}%"></div></div></div>
        <div class="processing-task-actions"><span class="badge ${processingTaskStatusClass(task.status)}">${processingTaskStatusText(task.status)}</span>${retryButton}</div>
      </div>
    `;
  }).join('');
}


function renderProcessingTaskCenter() {
  if (!processingTaskCenterBody) return;
  const items = processingTaskCenter.items || [];
  processingTaskCenterBody.innerHTML = processingTaskRowsHtml(items);
  if (processingTaskCenterBadge) processingTaskCenterBadge.textContent = `${processingTaskCenter.total || 0} 条`;
  if (processingTaskCenterPageInfo) processingTaskCenterPageInfo.textContent = `第 ${processingTaskCenter.page || 1} / ${processingTaskCenter.total_pages || 1} 页 · 共 ${processingTaskCenter.total || 0} 条`;
  if (processingTaskCenterPrev) processingTaskCenterPrev.disabled = (processingTaskCenter.page || 1) <= 1;
  if (processingTaskCenterNext) processingTaskCenterNext.disabled = (processingTaskCenter.page || 1) >= (processingTaskCenter.total_pages || 1);
}


async function loadProcessingTaskCenter(options = {}) {
  if (!processingTaskCenterBody) return;
  const nextPage = options.page || processingTaskCenter.page || 1;
  const params = new URLSearchParams({ page: String(nextPage), page_size: String(processingTaskCenter.page_size || 20) });
  if (processingTaskTypeFilter?.value) params.set('task_type', processingTaskTypeFilter.value);
  if (processingTaskStatusFilter?.value) params.set('status', processingTaskStatusFilter.value);
  try {
    processingTaskCenter = await fetchJson(`/api/processing-items/tasks?${params.toString()}`);
    renderProcessingTaskCenter();
  } catch (error) {
    processingTaskCenterBody.innerHTML = `<div class="empty-row">任务历史加载失败：${error.message}</div>`;
  }
}

async function retryProcessingTaskFailed(taskRef) {
  const [taskType, taskId] = String(taskRef || '').split(':');
  if (!taskType || !taskId) return;
  if (!await askConfirm('确认只重试这个任务里的失败商品吗？')) return;
  await fetchJson(`/api/processing-items/tasks/${taskType}/${taskId}/retry-failed`, { method: 'POST' });
  await loadProcessingTaskCenter();
  await notify('已创建失败项重试任务');
}

function renderProcessingItems() {
  if (!processingBody) return;
  const filteredItems = filteredProcessingItems();
  const pageItems = pagedProcessingItems();
  if (processingListBadge) processingListBadge.textContent = `${filteredItems.length} / ${processingItems.length}`;
  if (processingPageInfo) processingPageInfo.textContent = `第 ${processingPagination.page} / ${processingPagination.total_pages} 页 · 共 ${filteredItems.length} 个`;
  if (processingPrevPage) processingPrevPage.disabled = processingPagination.page <= 1;
  if (processingNextPage) processingNextPage.disabled = processingPagination.page >= processingPagination.total_pages;
  if (!pageItems.length) {
    processingBody.innerHTML = '<div class="empty-row">暂无商品处理数据，先从商品库或采集结果加入商品</div>';
    renderProcessingDetail(null);
    syncProcessingSelectAllState();
    return;
  }
  if (!selectedProcessingProductId || !filteredItems.some(item => item.product_id === selectedProcessingProductId)) {
    selectedProcessingProductId = pageItems[0].product_id;
  }
  const filteredIds = new Set(filteredItems.map(item => item.product_id));
  selectedProcessingIds = new Set(Array.from(selectedProcessingIds).filter(id => filteredIds.has(id)));
  processingBody.innerHTML = pageItems.map(item => {
    const imageOptions = item.image_options || [];
    const preview = item.main_image || imageOptions[0]?.preview_url || '';
    const checked = selectedProcessingIds.has(item.product_id) ? 'checked' : '';
    const cardClass = processingCardClass(item);
    const exceptionType = processingExceptionType(item);
    const exceptionTypeText = { title: '标题', spec: '规格', image: '图片', field: '字段', link: '链接', other: '异常' }[exceptionType] || '异常';
    const exceptionBadge = processingExceptionIds.has(item.product_id) ? `<span class="badge red">${exceptionTypeText}</span>` : '';
    return `
      <button class="processing-card ${cardClass} ${item.product_id === selectedProcessingProductId ? 'active' : ''}" data-processing-select="${item.product_id}">
        <input class="processing-select" type="checkbox" data-processing-check="${item.product_id}" ${checked} aria-label="选择商品 ${item.skc}">
        <span class="processing-card-delete" title="删除待处理商品" data-processing-delete="${item.product_id}">×</span>
        <div>${preview ? `<img src="${preview}" alt="${item.skc}" loading="lazy" referrerpolicy="no-referrer">` : '<span>无图</span>'}</div>
        <section>
          <strong>${item.skc}</strong>
          <p>${item.title}</p>
          <footer>${processingUploadBadge(item)}${exceptionBadge}<span>${imageOptions.length} 图</span></footer>
        </section>
      </button>
  `;
  }).join('');
  syncProcessingSelectAllState();
  renderProcessingDetail(filteredItems.find(item => item.product_id === selectedProcessingProductId));
}


const PLATFORM_COLOR_GROUPS = [
  {
    "name": "白色系",
    "colors": [
      "白色",
      "米白色",
      "乳白色",
      "象牙白"
    ]
  },
  {
    "name": "红色系",
    "colors": [
      "红色",
      "桔红色",
      "玫红色",
      "粉红色",
      "桃色",
      "蔷薇色",
      "深粉红",
      "胭脂色",
      "藕色",
      "西瓜红",
      "酒红色",
      "猩红色",
      "亮粉色",
      "洋红色",
      "珊瑚色",
      "橙红色",
      "砖红色",
      "深红色"
    ]
  },
  {
    "name": "黑色系",
    "colors": [
      "黑色"
    ]
  },
  {
    "name": "花色系",
    "colors": [
      "花色"
    ]
  },
  {
    "name": "黄色系",
    "colors": [
      "卡其色",
      "姜黄色",
      "明黄色",
      "杏色",
      "柠檬黄",
      "荧光黄",
      "金色",
      "香槟色",
      "黄色",
      "浅黄色",
      "小麦色",
      "橙色",
      "土黄色",
      "向日葵色",
      "肤色"
    ]
  },
  {
    "name": "灰色系",
    "colors": [
      "深灰色",
      "浅灰色",
      "奶奶灰",
      "灰色",
      "铅色",
      "石板灰",
      "银灰色",
      "深空灰",
      "石墨色"
    ]
  },
  {
    "name": "蓝色系",
    "colors": [
      "天蓝色",
      "孔雀蓝",
      "宝蓝色",
      "浅蓝色",
      "蓝色",
      "湖蓝色",
      "亮钢蓝",
      "道奇蓝",
      "深天蓝",
      "军服蓝",
      "蔚蓝色",
      "淡青色",
      "青色",
      "暗青色",
      "藏青色",
      "粉蓝色",
      "海蓝色",
      "中蓝色",
      "深蓝色"
    ]
  },
  {
    "name": "绿色系",
    "colors": [
      "军绿色",
      "墨绿色",
      "浅绿色",
      "绿色",
      "翠绿色",
      "孔雀绿",
      "荧光绿",
      "绿黄色",
      "草绿色",
      "黄绿色",
      "碧绿",
      "绿宝石",
      "海洋绿",
      "橄榄色",
      "橄榄绿",
      "抹茶色"
    ]
  },
  {
    "name": "透明系",
    "colors": [
      "透明"
    ]
  },
  {
    "name": "紫色系",
    "colors": [
      "浅紫色",
      "深紫色",
      "紫红色",
      "紫罗兰",
      "暗紫罗兰",
      "紫色",
      "深洋红色",
      "紫兰色",
      "熏衣草淡紫"
    ]
  },
  {
    "name": "棕色系",
    "colors": [
      "咖啡色",
      "巧克力色",
      "栗色",
      "深卡其布色",
      "浅棕色",
      "深棕色",
      "褐色",
      "棕褐色",
      "驼色",
      "橄榄棕色",
      "红褐色",
      "茶色",
      "亚麻色",
      "黄土赭色",
      "琥珀色",
      "小豆色",
      "焦糖色",
      "肉桂色",
      "玫瑰棕色",
      "玫瑰金",
      "古铜色"
    ]
  },
  {
    "name": "其他",
    "colors": [
      "混合色"
    ]
  }
];
const PLATFORM_STANDARD_COLORS = PLATFORM_COLOR_GROUPS.flatMap(group => group.colors);
const COLOR_ALIAS_ENTRIES = [
  [
    "白色",
    "白色"
  ],
  [
    "白",
    "白色"
  ],
  [
    "米白色",
    "米白色"
  ],
  [
    "米白",
    "米白色"
  ],
  [
    "乳白色",
    "乳白色"
  ],
  [
    "乳白",
    "乳白色"
  ],
  [
    "象牙白",
    "象牙白"
  ],
  [
    "红色",
    "红色"
  ],
  [
    "红",
    "红色"
  ],
  [
    "桔红色",
    "桔红色"
  ],
  [
    "桔红",
    "桔红色"
  ],
  [
    "玫红色",
    "玫红色"
  ],
  [
    "玫红",
    "玫红色"
  ],
  [
    "粉红色",
    "粉红色"
  ],
  [
    "粉红",
    "粉红色"
  ],
  [
    "桃色",
    "桃色"
  ],
  [
    "桃",
    "桃色"
  ],
  [
    "蔷薇色",
    "蔷薇色"
  ],
  [
    "蔷薇",
    "蔷薇色"
  ],
  [
    "深粉红",
    "深粉红"
  ],
  [
    "胭脂色",
    "胭脂色"
  ],
  [
    "胭脂",
    "胭脂色"
  ],
  [
    "藕色",
    "藕色"
  ],
  [
    "藕",
    "藕色"
  ],
  [
    "西瓜红",
    "西瓜红"
  ],
  [
    "酒红色",
    "酒红色"
  ],
  [
    "酒红",
    "酒红色"
  ],
  [
    "猩红色",
    "猩红色"
  ],
  [
    "猩红",
    "猩红色"
  ],
  [
    "亮粉色",
    "亮粉色"
  ],
  [
    "亮粉",
    "亮粉色"
  ],
  [
    "洋红色",
    "洋红色"
  ],
  [
    "洋红",
    "洋红色"
  ],
  [
    "珊瑚色",
    "珊瑚色"
  ],
  [
    "珊瑚",
    "珊瑚色"
  ],
  [
    "橙红色",
    "橙红色"
  ],
  [
    "橙红",
    "橙红色"
  ],
  [
    "砖红色",
    "砖红色"
  ],
  [
    "砖红",
    "砖红色"
  ],
  [
    "深红色",
    "深红色"
  ],
  [
    "深红",
    "深红色"
  ],
  [
    "黑色",
    "黑色"
  ],
  [
    "黑",
    "黑色"
  ],
  [
    "花色",
    "花色"
  ],
  [
    "花",
    "花色"
  ],
  [
    "卡其色",
    "卡其色"
  ],
  [
    "卡其",
    "卡其色"
  ],
  [
    "姜黄色",
    "姜黄色"
  ],
  [
    "姜黄",
    "姜黄色"
  ],
  [
    "明黄色",
    "明黄色"
  ],
  [
    "明黄",
    "明黄色"
  ],
  [
    "杏色",
    "杏色"
  ],
  [
    "杏",
    "杏色"
  ],
  [
    "柠檬黄",
    "柠檬黄"
  ],
  [
    "荧光黄",
    "荧光黄"
  ],
  [
    "金色",
    "金色"
  ],
  [
    "金",
    "金色"
  ],
  [
    "香槟色",
    "香槟色"
  ],
  [
    "香槟",
    "香槟色"
  ],
  [
    "黄色",
    "黄色"
  ],
  [
    "黄",
    "黄色"
  ],
  [
    "浅黄色",
    "浅黄色"
  ],
  [
    "浅黄",
    "浅黄色"
  ],
  [
    "小麦色",
    "小麦色"
  ],
  [
    "小麦",
    "小麦色"
  ],
  [
    "橙色",
    "橙色"
  ],
  [
    "橙",
    "橙色"
  ],
  [
    "土黄色",
    "土黄色"
  ],
  [
    "土黄",
    "土黄色"
  ],
  [
    "向日葵色",
    "向日葵色"
  ],
  [
    "向日葵",
    "向日葵色"
  ],
  [
    "肤色",
    "肤色"
  ],
  [
    "肤",
    "肤色"
  ],
  [
    "深灰色",
    "深灰色"
  ],
  [
    "深灰",
    "深灰色"
  ],
  [
    "浅灰色",
    "浅灰色"
  ],
  [
    "浅灰",
    "浅灰色"
  ],
  [
    "奶奶灰",
    "奶奶灰"
  ],
  [
    "灰色",
    "灰色"
  ],
  [
    "灰",
    "灰色"
  ],
  [
    "铅色",
    "铅色"
  ],
  [
    "铅",
    "铅色"
  ],
  [
    "石板灰",
    "石板灰"
  ],
  [
    "银灰色",
    "银灰色"
  ],
  [
    "银灰",
    "银灰色"
  ],
  [
    "深空灰",
    "深空灰"
  ],
  [
    "石墨色",
    "石墨色"
  ],
  [
    "石墨",
    "石墨色"
  ],
  [
    "天蓝色",
    "天蓝色"
  ],
  [
    "天蓝",
    "天蓝色"
  ],
  [
    "孔雀蓝",
    "孔雀蓝"
  ],
  [
    "宝蓝色",
    "宝蓝色"
  ],
  [
    "宝蓝",
    "宝蓝色"
  ],
  [
    "浅蓝色",
    "浅蓝色"
  ],
  [
    "浅蓝",
    "浅蓝色"
  ],
  [
    "蓝色",
    "蓝色"
  ],
  [
    "蓝",
    "蓝色"
  ],
  [
    "湖蓝色",
    "湖蓝色"
  ],
  [
    "湖蓝",
    "湖蓝色"
  ],
  [
    "亮钢蓝",
    "亮钢蓝"
  ],
  [
    "道奇蓝",
    "道奇蓝"
  ],
  [
    "深天蓝",
    "深天蓝"
  ],
  [
    "军服蓝",
    "军服蓝"
  ],
  [
    "蔚蓝色",
    "蔚蓝色"
  ],
  [
    "蔚蓝",
    "蔚蓝色"
  ],
  [
    "淡青色",
    "淡青色"
  ],
  [
    "淡青",
    "淡青色"
  ],
  [
    "青色",
    "青色"
  ],
  [
    "青",
    "青色"
  ],
  [
    "暗青色",
    "暗青色"
  ],
  [
    "暗青",
    "暗青色"
  ],
  [
    "藏青色",
    "藏青色"
  ],
  [
    "藏青",
    "藏青色"
  ],
  [
    "粉蓝色",
    "粉蓝色"
  ],
  [
    "粉蓝",
    "粉蓝色"
  ],
  [
    "海蓝色",
    "海蓝色"
  ],
  [
    "海蓝",
    "海蓝色"
  ],
  [
    "中蓝色",
    "中蓝色"
  ],
  [
    "中蓝",
    "中蓝色"
  ],
  [
    "深蓝色",
    "深蓝色"
  ],
  [
    "深蓝",
    "深蓝色"
  ],
  [
    "军绿色",
    "军绿色"
  ],
  [
    "军绿",
    "军绿色"
  ],
  [
    "墨绿色",
    "墨绿色"
  ],
  [
    "墨绿",
    "墨绿色"
  ],
  [
    "浅绿色",
    "浅绿色"
  ],
  [
    "浅绿",
    "浅绿色"
  ],
  [
    "绿色",
    "绿色"
  ],
  [
    "绿",
    "绿色"
  ],
  [
    "翠绿色",
    "翠绿色"
  ],
  [
    "翠绿",
    "翠绿色"
  ],
  [
    "孔雀绿",
    "孔雀绿"
  ],
  [
    "荧光绿",
    "荧光绿"
  ],
  [
    "绿黄色",
    "绿黄色"
  ],
  [
    "绿黄",
    "绿黄色"
  ],
  [
    "草绿色",
    "草绿色"
  ],
  [
    "草绿",
    "草绿色"
  ],
  [
    "黄绿色",
    "黄绿色"
  ],
  [
    "黄绿",
    "黄绿色"
  ],
  [
    "碧绿",
    "碧绿"
  ],
  [
    "绿宝石",
    "绿宝石"
  ],
  [
    "海洋绿",
    "海洋绿"
  ],
  [
    "橄榄色",
    "橄榄色"
  ],
  [
    "橄榄",
    "橄榄色"
  ],
  [
    "橄榄绿",
    "橄榄绿"
  ],
  [
    "抹茶色",
    "抹茶色"
  ],
  [
    "抹茶",
    "抹茶色"
  ],
  [
    "透明",
    "透明"
  ],
  [
    "浅紫色",
    "浅紫色"
  ],
  [
    "浅紫",
    "浅紫色"
  ],
  [
    "深紫色",
    "深紫色"
  ],
  [
    "深紫",
    "深紫色"
  ],
  [
    "紫红色",
    "紫红色"
  ],
  [
    "紫红",
    "紫红色"
  ],
  [
    "紫罗兰",
    "紫罗兰"
  ],
  [
    "暗紫罗兰",
    "暗紫罗兰"
  ],
  [
    "紫色",
    "紫色"
  ],
  [
    "紫",
    "紫色"
  ],
  [
    "深洋红色",
    "深洋红色"
  ],
  [
    "深洋红",
    "深洋红色"
  ],
  [
    "紫兰色",
    "紫兰色"
  ],
  [
    "紫兰",
    "紫兰色"
  ],
  [
    "熏衣草淡紫",
    "熏衣草淡紫"
  ],
  [
    "咖啡色",
    "咖啡色"
  ],
  [
    "咖啡",
    "咖啡色"
  ],
  [
    "巧克力色",
    "巧克力色"
  ],
  [
    "巧克力",
    "巧克力色"
  ],
  [
    "栗色",
    "栗色"
  ],
  [
    "栗",
    "栗色"
  ],
  [
    "深卡其布色",
    "深卡其布色"
  ],
  [
    "深卡其布",
    "深卡其布色"
  ],
  [
    "浅棕色",
    "浅棕色"
  ],
  [
    "浅棕",
    "浅棕色"
  ],
  [
    "深棕色",
    "深棕色"
  ],
  [
    "深棕",
    "深棕色"
  ],
  [
    "褐色",
    "褐色"
  ],
  [
    "褐",
    "褐色"
  ],
  [
    "棕褐色",
    "棕褐色"
  ],
  [
    "棕褐",
    "棕褐色"
  ],
  [
    "驼色",
    "驼色"
  ],
  [
    "驼",
    "驼色"
  ],
  [
    "橄榄棕色",
    "橄榄棕色"
  ],
  [
    "橄榄棕",
    "橄榄棕色"
  ],
  [
    "红褐色",
    "红褐色"
  ],
  [
    "红褐",
    "红褐色"
  ],
  [
    "茶色",
    "茶色"
  ],
  [
    "茶",
    "茶色"
  ],
  [
    "亚麻色",
    "亚麻色"
  ],
  [
    "亚麻",
    "亚麻色"
  ],
  [
    "黄土赭色",
    "黄土赭色"
  ],
  [
    "黄土赭",
    "黄土赭色"
  ],
  [
    "琥珀色",
    "琥珀色"
  ],
  [
    "琥珀",
    "琥珀色"
  ],
  [
    "小豆色",
    "小豆色"
  ],
  [
    "小豆",
    "小豆色"
  ],
  [
    "焦糖色",
    "焦糖色"
  ],
  [
    "焦糖",
    "焦糖色"
  ],
  [
    "肉桂色",
    "肉桂色"
  ],
  [
    "肉桂",
    "肉桂色"
  ],
  [
    "玫瑰棕色",
    "玫瑰棕色"
  ],
  [
    "玫瑰棕",
    "玫瑰棕色"
  ],
  [
    "玫瑰金",
    "玫瑰金"
  ],
  [
    "古铜色",
    "古铜色"
  ],
  [
    "古铜",
    "古铜色"
  ],
  [
    "混合色",
    "混合色"
  ],
  [
    "混合",
    "混合色"
  ],
  [
    "white",
    "白色"
  ],
  [
    "purewhite",
    "白色"
  ],
  [
    "offwhite",
    "米白色"
  ],
  [
    "milkywhite",
    "乳白色"
  ],
  [
    "cream",
    "乳白色"
  ],
  [
    "ivory",
    "象牙白"
  ],
  [
    "red",
    "红色"
  ],
  [
    "orangered",
    "桔红色"
  ],
  [
    "rose red",
    "玫红色"
  ],
  [
    "rosered",
    "玫红色"
  ],
  [
    "pink",
    "粉红色"
  ],
  [
    "hotpink",
    "深粉红"
  ],
  [
    "magenta",
    "洋红色"
  ],
  [
    "coral",
    "珊瑚色"
  ],
  [
    "burgundy",
    "酒红色"
  ],
  [
    "wine red",
    "酒红色"
  ],
  [
    "winered",
    "酒红色"
  ],
  [
    "scarlet",
    "猩红色"
  ],
  [
    "black",
    "黑色"
  ],
  [
    "blk",
    "黑色"
  ],
  [
    "multi",
    "花色"
  ],
  [
    "multicolor",
    "花色"
  ],
  [
    "mixed",
    "混合色"
  ],
  [
    "mixedcolor",
    "混合色"
  ],
  [
    "khaki",
    "卡其色"
  ],
  [
    "mustard",
    "姜黄色"
  ],
  [
    "lemonyellow",
    "柠檬黄"
  ],
  [
    "neonyellow",
    "荧光黄"
  ],
  [
    "gold",
    "金色"
  ],
  [
    "champagne",
    "香槟色"
  ],
  [
    "yellow",
    "黄色"
  ],
  [
    "lightyellow",
    "浅黄色"
  ],
  [
    "wheat",
    "小麦色"
  ],
  [
    "orange",
    "橙色"
  ],
  [
    "earthyellow",
    "土黄色"
  ],
  [
    "skin",
    "肤色"
  ],
  [
    "nude",
    "肤色"
  ],
  [
    "darkgray",
    "深灰色"
  ],
  [
    "darkgrey",
    "深灰色"
  ],
  [
    "lightgray",
    "浅灰色"
  ],
  [
    "lightgrey",
    "浅灰色"
  ],
  [
    "gray",
    "灰色"
  ],
  [
    "grey",
    "灰色"
  ],
  [
    "silvergray",
    "银灰色"
  ],
  [
    "spacegray",
    "深空灰"
  ],
  [
    "graphite",
    "石墨色"
  ],
  [
    "skyblue",
    "天蓝色"
  ],
  [
    "peacockblue",
    "孔雀蓝"
  ],
  [
    "royalblue",
    "宝蓝色"
  ],
  [
    "lightblue",
    "浅蓝色"
  ],
  [
    "blue",
    "蓝色"
  ],
  [
    "lakeblue",
    "湖蓝色"
  ],
  [
    "dodgerblue",
    "道奇蓝"
  ],
  [
    "deepskyblue",
    "深天蓝"
  ],
  [
    "navy",
    "藏青色"
  ],
  [
    "navyblue",
    "藏青色"
  ],
  [
    "azure",
    "蔚蓝色"
  ],
  [
    "cyan",
    "青色"
  ],
  [
    "darkcyan",
    "暗青色"
  ],
  [
    "powderblue",
    "粉蓝色"
  ],
  [
    "oceanblue",
    "海蓝色"
  ],
  [
    "mediumblue",
    "中蓝色"
  ],
  [
    "darkblue",
    "深蓝色"
  ],
  [
    "denimblue",
    "蓝色"
  ],
  [
    "armygreen",
    "军绿色"
  ],
  [
    "darkgreen",
    "墨绿色"
  ],
  [
    "lightgreen",
    "浅绿色"
  ],
  [
    "green",
    "绿色"
  ],
  [
    "emerald",
    "绿宝石"
  ],
  [
    "neongreen",
    "荧光绿"
  ],
  [
    "grassgreen",
    "草绿色"
  ],
  [
    "yellowgreen",
    "黄绿色"
  ],
  [
    "seagreen",
    "海洋绿"
  ],
  [
    "olive",
    "橄榄色"
  ],
  [
    "olivegreen",
    "橄榄绿"
  ],
  [
    "matcha",
    "抹茶色"
  ],
  [
    "clear",
    "透明"
  ],
  [
    "transparent",
    "透明"
  ],
  [
    "lightpurple",
    "浅紫色"
  ],
  [
    "darkpurple",
    "深紫色"
  ],
  [
    "purple",
    "紫色"
  ],
  [
    "violet",
    "紫罗兰"
  ],
  [
    "darkviolet",
    "暗紫罗兰"
  ],
  [
    "lavender",
    "熏衣草淡紫"
  ],
  [
    "brown",
    "褐色"
  ],
  [
    "coffee",
    "咖啡色"
  ],
  [
    "chocolate",
    "巧克力色"
  ],
  [
    "maroon",
    "栗色"
  ],
  [
    "lightbrown",
    "浅棕色"
  ],
  [
    "darkbrown",
    "深棕色"
  ],
  [
    "camel",
    "驼色"
  ],
  [
    "linen",
    "亚麻色"
  ],
  [
    "amber",
    "琥珀色"
  ],
  [
    "caramel",
    "焦糖色"
  ],
  [
    "cinnamon",
    "肉桂色"
  ],
  [
    "rosegold",
    "玫瑰金"
  ],
  [
    "bronze",
    "古铜色"
  ]
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

function safeSkuSegment(value, fallback = 'ITEM') {
  const text = String(value || '').trim() || fallback;
  return text.replace(/[<>:"/\\|?*\x00-\x1f]/g, '_').replace(/\s+/g, '_').replace(/^[ ._]+|[ ._]+$/g, '').slice(0, 80) || fallback;
}

const COLOR_ENGLISH_MAP = new Map();
COLOR_ALIAS_ENTRIES.forEach(([alias, color]) => {
  if (/^[A-Za-z][A-Za-z\s_-]*$/.test(String(alias || '')) && !COLOR_ENGLISH_MAP.has(color)) {
    COLOR_ENGLISH_MAP.set(color, safeSkuSegment(alias, color).toLowerCase());
  }
});

function colorEnglishLabel(value) {
  const color = normalizeKnownColor(value) || String(value || '').trim();
  if (!color) return 'COLOR';
  return (COLOR_ENGLISH_MAP.get(color) || safeSkuSegment(color, 'COLOR')).toUpperCase();
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

const STANDARD_UPLOAD_SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];
const STANDARD_UPLOAD_SIZE_RANK = new Map(STANDARD_UPLOAD_SIZES.map((size, index) => [size, index]));
const SIZE_ALIAS_MAP = new Map([
  ['XS', 'XS'], ['S', 'S'], ['M', 'M'], ['L', 'L'], ['XL', 'XL'], ['XXL', 'XXL'],
  ['2XL', 'XXL'], ['XXXL', 'XXL'], ['3XL', 'XXL'], ['4XL', 'XXL'],
]);

function normalizeUploadSize(value) {
  let text = String(value || '').trim().toUpperCase();
  if (!text) return '';
  text = text.replace(/[?\[].*?[?\]]/g, '').trim();
  const match = text.match(/(^|[^A-Z0-9])(XS|S|M|L|XL|XXL|2XL|3XL|4XL|XXXL)(?![A-Z0-9])/) || text.match(/(XS|S|M|L|XL|XXL|2XL|3XL|4XL|XXXL)/);
  if (!match) return text;
  const size = match[2] || match[1];
  return SIZE_ALIAS_MAP.get(size) || size;
}

function sortUploadSizes(sizes) {
  return uniqueList(sizes).sort((left, right) => {
    const leftSize = normalizeUploadSize(left);
    const rightSize = normalizeUploadSize(right);
    const leftRank = STANDARD_UPLOAD_SIZE_RANK.has(leftSize) ? STANDARD_UPLOAD_SIZE_RANK.get(leftSize) : STANDARD_UPLOAD_SIZES.length;
    const rightRank = STANDARD_UPLOAD_SIZE_RANK.has(rightSize) ? STANDARD_UPLOAD_SIZE_RANK.get(rightSize) : STANDARD_UPLOAD_SIZES.length;
    if (leftRank !== rightRank) return leftRank - rightRank;
    return String(left).localeCompare(String(right), 'zh-Hans-CN', { numeric: true });
  });
}

function cleanSpecLabel(value, type) {
  const text = String(value || '').trim();
  if (!text) return '';
  const pattern = type === 'color' ? /\u989c\u8272[:\uff1a]([^;\/]+)/ : /\u5c3a\u7801[:\uff1a]([^;\/]+)/;
  const match = text.match(pattern);
  const label = (match ? match[1] : text).replace(/[()??]/g, '').trim();
  return type === 'color' ? normalizeKnownColor(label) : normalizeUploadSize(label);
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
    if (!key && String(color || '').trim().toLowerCase() !== 'pending') return null;
    const colorKey = key || '混合色';
    if (!colorMap.has(colorKey)) colorMap.set(colorKey, { color: colorKey, images: [], imageUrls: new Set(), sizes: new Set(), skuIds: new Set() });
    return colorMap.get(colorKey);
  };
  globalColors.forEach(color => ensureColor(color));
  (item.color_image_assignments || [])
    .slice()
    .sort((left, right) => Number(left.sort_order || 0) - Number(right.sort_order || 0))
    .forEach(assignment => {
      const entry = ensureColor(assignment.color);
      const imageUrl = assignment.image_url || assignment.url || '';
      if (!entry || !imageUrl || entry.imageUrls.has(imageUrl)) return;
      entry.imageUrls.add(imageUrl);
      entry.images.push({
        url: imageUrl,
        preview_url: assignment.preview_url || assignment.previewUrl || imageUrl,
        kind: assignment.source || 'color_assignment',
        color: assignment.color,
        size: '',
        sku_id: '',
      });
    });
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
  if (!colorMap.size && !globalColors.length && (item.main_image || (item.image_options || []).length)) ensureColor('混合色');
  if (!colorMap.size) return { colors: [], sizes: globalSizes, rows: [] };
  const colorEntries = Array.from(colorMap.values()).map(entry => ({
    color: entry.color,
    images: entry.images,
    sizes: sortUploadSizes(Array.from(entry.sizes)),
    skuIds: Array.from(entry.skuIds),
  }));
  const allSizes = sortUploadSizes([...globalSizes, ...colorEntries.flatMap(entry => entry.sizes)]);
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
      const displayCount = Math.max(5, assignedImages.length + 1);
      const slotImages = Array.from({ length: displayCount }, (_slot, index) => assignedImages.find(option => Number(option.sort_order) === index) || assignedImages[index] || null);
      return `<div class="skc-row"><div class="skc-color"><b>${entry.color}</b><small>${assignedImages.length ? `已分图 ${assignedImages.length} 张` : (entry.sizes.length ? entry.sizes.join(' / ') : '尺码待识别')}</small></div><div class="skc-code">${item.skc}-${entry.color}</div><div class="skc-images skc-slots">${slotImages.map((option, index) => {
        if (!option) return `<button class="skc-image skc-slot empty" data-skc-drop-slot="true" data-product-id="${item.product_id}" data-color="${entry.color}" data-slot-index="${index}" aria-label="添加${entry.color}颜色图 #${index + 1}"><span class="slot-title">#${index + 1}</span><em>拖入或点击加号</em><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="选择图片">+</strong></button>`;
        const imageUrl = option.image_url || option.url;
        const imageSrc = option.preview_url || option.previewUrl || imageUrl;
        const selected = selectedImageUrls.has(imageUrl);
        return `<button class="skc-image skc-slot image-select-card ${selected ? 'active' : ''}" data-skc-drop-slot="true" data-product-id="${item.product_id}" data-color="${entry.color}" data-slot-index="${index}" data-processing-image-pick="${item.product_id}" data-image-url="${imageUrl}" aria-label="${entry.color}颜色图 #${index + 1}"><img src="${imageSrc}" alt="${entry.color} #${index + 1}" loading="lazy" referrerpolicy="no-referrer" data-preview-image="${imageSrc}" data-preview-title="${entry.color} #${index + 1}"><span class="slot-title">#${index + 1}</span><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="更换图片">+</strong><i class="slot-action slot-delete" data-clear-skc-slot="true" aria-label="删除图片">×</i></button>`;
      }).join('')}</div></div>`;
    }).join('')
    : '<div class="desc">暂未识别颜色图片</div>';
  const sizeChips = matrix.sizes.length
    ? matrix.sizes.map(size => `<span class="size-chip active">✓ ${size}</span>`).join('')
    : '<span class="desc">尺码待识别</span>';
  const variantRows = matrix.rows.length
    ? matrix.rows.map(row => `<tr><td>${row.color}</td><td>${row.size}</td><td>${item.skc}-${colorEnglishLabel(row.color)}-${safeSkuSegment(row.size, 'SIZE')}</td><td>${row.image ? '<span class="badge green">有图</span>' : '<span class="badge red">待补图</span>'}</td><td>${Number(item.declared_price).toFixed(2)}</td><td>${item.stock}</td></tr>`).join('')
    : '<tr><td class="empty-row" colspan="6">暂无变种明细</td></tr>';
  const detailAssignments = item.detail_image_assignments || [];
  const detailOptions = detailAssignments.length ? detailAssignments : descOptions;
  const visibleDetailOptions = detailOptions
    .map((option, index) => ({ option, index }))
    .filter(({ option }) => option && (option.image_url || option.url));
  const detailCards = visibleDetailOptions.map(({ option, index }, displayIndex) => {
    const slotIndex = Number(option.sort_order ?? index);
    const imageUrl = option.image_url || option.url || '';
    const imageSrc = option.preview_url || option.previewUrl || imageUrl;
    const selected = selectedImageUrls.has(imageUrl);
    return `<button class="carousel-image detail-slot image-select-card ${selected ? 'active' : ''}" draggable="true" data-draggable-image="true" data-detail-drop-slot="true" data-product-id="${item.product_id}" data-slot-index="${slotIndex}" data-processing-image-pick="${item.product_id}" data-image-url="${imageUrl}" aria-label="详情图 #${displayIndex + 1}"><img src="${imageSrc}" alt="详情图 #${displayIndex + 1}" loading="lazy" referrerpolicy="no-referrer" data-preview-image="${imageSrc}" data-preview-title="详情图 #${displayIndex + 1}"><span class="slot-title">详情图 #${displayIndex + 1}</span><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="更换图片">+</strong><i class="slot-action slot-delete" data-clear-detail-slot="true" aria-label="删除图片">×</i></button>`;
  }).join('');
  const nextDetailSlotIndex = visibleDetailOptions.length;
  const addDetailCard = `<button class="carousel-image detail-slot empty detail-add-slot" data-detail-drop-slot="true" data-product-id="${item.product_id}" data-slot-index="${nextDetailSlotIndex}" aria-label="添加详情图"><span class="slot-title">添加详情图</span><small>拖入图片或点击加号选择</small><strong class="slot-action slot-add" data-open-slot-picker="true" aria-label="选择图片">+</strong></button>`;
  const detailSlotCount = visibleDetailOptions.length;
  const exception = processingExceptionMap.get(item.product_id);
  const exceptionLines = exception ? [...(exception.issues || []), ...(exception.warnings || [])] : [];
  const hasSpecException = exceptionLines.some(line => /颜色|尺码|标准色/.test(line));
  const specMapButton = hasSpecException ? '<button class="btn outline-blue" data-open-spec-mapping="true">查看规格映射</button>' : '';
  const exceptionBlock = exceptionLines.length ? `<section class="detail-block wide"><h3>异常修复建议</h3><div class="spec-summary">${exceptionLines.map(line => `<span><b>${line}</b></span>`).join('')}</div><div class="actions"><button class="btn primary" data-edit-processing-fields="${item.product_id}">编辑字段</button><button class="btn ghost" data-fix-processing-title="${item.product_id}">生成标题</button><button class="btn outline-blue" data-focus-processing-images="${item.product_id}">定位图片区</button>${specMapButton}</div></section>` : '';
  processingDetailPanel.innerHTML = `
    <div class="processing-detail-grid">
      ${exceptionBlock}
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
    body: JSON.stringify({ ids, status: bulkProductStatus?.value || productStatusFilter?.value || '待处理' }),
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
  const executableStatuses = ['blocked', 'empty', 'failed', 'cancelled'];
  const cancellableStatuses = ['queued', 'running'];
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
      <td><button class="btn ghost" data-collection-events="${task.id}">\u660e\u7ec6</button>${task.mode === '1688' && executableStatuses.includes(task.status) ? `<button class="btn ghost" data-collection-execute="${task.id}">\u91cd\u8bd5</button>` : ''}${task.mode === '1688' && cancellableStatuses.includes(task.status) ? `<button class="btn ghost" data-collection-cancel="${task.id}">\u53d6\u6d88</button>` : ''}</td>
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
async function refreshProcessingItem(productId) {
  const updated = await fetchJson(`/api/processing-items/by-id/${Number(productId)}`);
  const index = processingItems.findIndex(item => item.product_id === updated.product_id);
  if (index >= 0) processingItems[index] = updated;
  else processingItems.unshift(updated);
  try {
    await syncProcessingExceptionState();
  } catch (error) {
    console.warn('processing item preflight refresh failed', error);
  }
  renderProcessingItems();
}

async function syncProcessingExceptionState() {
  processingPreflightSummary = await fetchJson('/api/processing-items/preflight', { method: 'POST' });
  const exceptions = await fetchJson('/api/processing-items/exceptions?status=open');
  processingExceptionIds = new Set((exceptions || []).map(item => Number(item.product_id)));
  processingExceptionMap = new Map((exceptions || []).map(item => [Number(item.product_id), item]));
  return processingPreflightSummary;
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
    try {
      await syncProcessingExceptionState();
    } catch (preflightError) {
      console.warn('processing preflight failed', preflightError);
    }
    processingPagination.page_size = Number(processingPageSize?.value || processingPagination.page_size || 50);
    const params = new URLSearchParams({
      page: String(processingPagination.page || 1),
      page_size: String(processingPagination.page_size),
    });
    const keyword = String(processingSearchInput?.value || '').trim();
    const statusFilter = processingStatusFilter?.value || '';
    const exceptionType = processingExceptionTypeFilter?.value || '';
    if (keyword) params.set('q', keyword);
    if (statusFilter) params.set('status', statusFilter);
    if (exceptionType) params.set('exception_type', exceptionType);
    const pageData = await fetchJson(`/api/processing-items?${params.toString()}`);
    if (Array.isArray(pageData)) {
      processingItems = pageData;
      processingPagination.total = processingItems.length;
      processingPagination.page = 1;
      processingPagination.total_pages = 1;
    } else {
      processingItems = pageData.items || [];
      processingPagination.total = Number(pageData.total || processingItems.length || 0);
      processingPagination.page = Number(pageData.page || processingPagination.page || 1);
      processingPagination.page_size = Number(pageData.page_size || processingPagination.page_size || 50);
      processingPagination.total_pages = Number(pageData.total_pages || 1);
    }
    if (showFeedback && processingPreflightSummary) {
      addOperationLog('处理预检', processingPreflightSummary.blocked_count ? 'error' : 'success', `可处理 ${processingPreflightSummary.ready_count || 0} 个，异常 ${processingPreflightSummary.blocked_count || 0} 个，预警 ${Object.keys(processingPreflightSummary.warning_counts || {}).length} 类`, 35);
    }
    renderProcessingItems();
    if (showFeedback) await notify(`商品处理已刷新，共 ${processingPagination.total || processingItems.length} 条`);
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


async function importFreightFile(file) {
  if (!file) return;
  const zone = window.prompt('默认尾程 Zone（zone1~zone9），先默认 zone5', 'zone5') || 'zone5';
  const data = new FormData();
  data.append('file', file);
  data.append('default_zone', zone);
  const response = await fetch('/api/products/freight/import-file', { method: 'POST', body: data });
  const result = await response.json();
  if (!response.ok) throw new Error(result.detail || '导入运费表失败');
  await loadProducts();
  await loadFreightRules();
  await notify(`运费表已导入\n头程规则：${result.first_mile_count}\n尾程规则：${result.last_mile_count}\n默认 Zone：${result.default_zone}\n已自动刷新商品库利润`);
}

function freightNumber(value, fallback = 0) {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
}

function renderFirstMileEditor(rules = []) {
  if (!firstMileRuleEditor) return;
  const rows = rules.length ? rules : [{ channel: '空运', max_weight_g: 10000000, price_per_kg: 69, fixed_fee: 4 }];
  firstMileRuleEditor.innerHTML = rows.map(rule => `
    <div class="freight-rule-row first-mile-rule-row">
      <input class="input" data-field="channel" value="${rule.channel || '空运'}" placeholder="渠道" />
      <input class="input" data-field="max_weight_g" type="number" value="${rule.max_weight_g || 0}" placeholder="最大重量g" />
      <input class="input" data-field="price_per_kg" type="number" step="0.01" value="${rule.price_per_kg || 0}" placeholder="价格/kg" />
      <input class="input" data-field="fixed_fee" type="number" step="0.01" value="${rule.fixed_fee || 0}" placeholder="附加费" />
      <button class="btn ghost" type="button" data-remove-freight-row>删除</button>
    </div>
  `).join('');
}

function renderLastMileEditor(rules = []) {
  if (!lastMileRuleEditor) return;
  const rows = rules.length ? rules : [{ channel: 'Temu', max_weight_g: 0, zones: {} }];
  lastMileRuleEditor.innerHTML = rows.map(rule => `
    <div class="freight-rule-row last-mile-rule-row">
      <input class="input" data-field="channel" value="${rule.channel || 'Temu'}" placeholder="渠道" />
      <input class="input" data-field="max_weight_g" type="number" value="${rule.max_weight_g || 0}" placeholder="最大重量g" />
      ${FREIGHT_ZONES.map(zone => `<input class="input" data-zone="${zone}" type="number" step="0.01" value="${rule.zones?.[zone] ?? ''}" placeholder="${zone}" />`).join('')}
      <button class="btn ghost" type="button" data-remove-freight-row>删除</button>
    </div>
  `).join('');
}

function renderFreightEditor(data = {}) {
  if (freightDefaultZone) freightDefaultZone.value = data.default_zone || 'zone5';
  if (freightWarehouseFee) freightWarehouseFee.value = data.warehouse_fee ?? 15;
  renderFirstMileEditor(data.first_mile || []);
  renderLastMileEditor(data.last_mile || []);
}

function collectFreightRules() {
  const first_mile = Array.from(firstMileRuleEditor?.querySelectorAll('.first-mile-rule-row') || []).map(row => ({
    channel: row.querySelector('[data-field="channel"]')?.value?.trim() || '空运',
    max_weight_g: freightNumber(row.querySelector('[data-field="max_weight_g"]')?.value, 0),
    price_per_kg: freightNumber(row.querySelector('[data-field="price_per_kg"]')?.value, 0),
    fixed_fee: freightNumber(row.querySelector('[data-field="fixed_fee"]')?.value, 0),
  })).filter(rule => rule.max_weight_g > 0);
  const last_mile = Array.from(lastMileRuleEditor?.querySelectorAll('.last-mile-rule-row') || []).map(row => {
    const zones = {};
    FREIGHT_ZONES.forEach(zone => {
      zones[zone] = freightNumber(row.querySelector(`[data-zone="${zone}"]`)?.value, 0);
    });
    return {
      channel: row.querySelector('[data-field="channel"]')?.value?.trim() || 'Temu',
      max_weight_g: freightNumber(row.querySelector('[data-field="max_weight_g"]')?.value, 0),
      zones,
    };
  }).filter(rule => rule.max_weight_g > 0);
  return {
    default_zone: freightDefaultZone?.value || 'zone5',
    warehouse_fee: freightNumber(freightWarehouseFee?.value, 15),
    first_mile,
    last_mile,
  };
}

async function saveFreightRules() {
  const payload = collectFreightRules();
  if (!payload.first_mile.length) throw new Error('至少需要 1 条头程规则');
  const result = await fetchJson('/api/products/freight/rules', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  await loadProducts();
  renderFreightRules(result);
  await notify(`运费模板已保存\n已刷新商品：${result.updated_count || 0}\n头程规则：${result.first_mile_count || 0}\n尾程规则：${result.last_mile_count || 0}`);
}

function renderFreightRules(data = {}) {
  renderFreightEditor(data || {});
  if (freightRuleSummary) {
    freightRuleSummary.innerHTML = `
      <div class="metric-card"><span>默认尾程 Zone</span><b>${data.default_zone || 'zone5'}</b><em>用于自动核价</em></div>
      <div class="metric-card"><span>仓库操作费</span><b>${money(data.warehouse_fee ?? 15)}</b><em>默认按件计费</em></div>
      <div class="metric-card"><span>头程规则</span><b>${data.first_mile_count || 0}</b><em>价格/kg + 附加费</em></div>
      <div class="metric-card"><span>尾程规则</span><b>${data.last_mile_count || 0}</b><em>按重量档匹配</em></div>
    `;
  }
  if (!freightRuleDetails) return;
  const firstRows = (data.first_mile || []).map(rule => `<span class="spec-chip">${rule.channel || '头程'} ≤ ${rule.max_weight_g}g：${rule.price_per_kg}/kg + ${rule.fixed_fee}</span>`).join('');
  const lastRows = (data.last_mile || []).slice(0, 30).map(rule => {
    const zone = data.default_zone || 'zone5';
    const zoneValue = rule.zones ? rule.zones[zone] : '';
    return `<span class="spec-chip">${rule.channel || '尾程'} ≤ ${rule.max_weight_g}g：${zone} = ${zoneValue || '-'}</span>`;
  }).join('');
  freightRuleDetails.innerHTML = `
    <div class="spec-map-group"><div class="spec-map-group-title"><b>头程规则</b><span>${data.first_mile_count || 0} 条</span></div><div class="spec-chip-list">${firstRows || '<span class="desc">暂无头程规则</span>'}</div></div>
    <div class="spec-map-group"><div class="spec-map-group-title"><b>尾程规则</b><span>${data.last_mile_count || 0} 条</span></div><div class="spec-chip-list">${lastRows || '<span class="desc">暂无尾程规则</span>'}</div></div>
  `;
}

async function loadFreightRules() {
  if (!freightRuleSummary && !freightRuleDetails) return;
  try {
    renderFreightRules(await fetchJson('/api/products/freight/rules'));
  } catch (error) {
    if (freightRuleDetails) freightRuleDetails.innerHTML = `<div class="empty-row">运费规则加载失败：${error.message || error}</div>`;
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

function collectionFilterParams() {
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
  return params;
}

async function selectFilteredCollectionItems() {
  const params = collectionFilterParams();
  params.set('limit', '20000');
  const result = await fetchJson(`/api/collection-items/ids?${params}`);
  const ids = result.ids || [];
  ids.forEach(id => selectedCollectionIdsSet.add(Number(id)));
  renderCollectionItems();
  await notify(`\u5df2\u9009\u4e2d\u5f53\u524d\u7b5b\u9009\u6761\u4ef6\u4e0b ${ids.length} \u6761\u91c7\u96c6\u7ed3\u679c${result.total > ids.length ? `\uff08\u603b ${result.total} \u6761\uff0c\u672c\u6b21\u6700\u591a\u9009\u4e2d ${ids.length} \u6761\uff09` : ''}`);
}

function clearCollectionSelection() {
  selectedCollectionIdsSet.clear();
  renderCollectionItems();
}

async function loadCollectionItems(options = {}) {
  if (!collectionBody) return;
  if (options.resetPage) collectionPagination.page = 1;
  const params = collectionFilterParams();
  params.set('page', String(collectionPagination.page || 1));
  params.set('page_size', String(collectionPagination.page_size || Number(collectionPageSizeSelect?.value || 50)));
  const result = await fetchJson(`/api/collection-items?${params}`);
  if (Array.isArray(result)) {
    collectionItems = result;
    collectionPagination = { page: 1, page_size: result.length || 50, total: result.length, total_pages: 1 };
  } else {
    collectionItems = result.items || [];
    collectionPagination = {
      page: result.page || 1,
      page_size: result.page_size || 50,
      total: result.total || 0,
      total_pages: result.total_pages || 1,
    };
  }
  renderCollectionItems();
}



function selectedCollectionIds() {
  document.querySelectorAll('[data-collection-id]').forEach(input => {
    const id = Number(input.dataset.collectionId);
    if (!id) return;
    if (input.checked) selectedCollectionIdsSet.add(id);
    else selectedCollectionIdsSet.delete(id);
  });
  return Array.from(selectedCollectionIdsSet);
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

async function refreshCollectionTaskEvents(taskId) {
  try {
    const events = await fetchJson(`/api/collection-tasks/${taskId}/events`);
    collectionTaskEventsCache.set(Number(taskId), events || []);
  } catch (error) {
    console.warn('refreshCollectionTaskEvents failed', error);
  }
}

async function refreshCollectionTaskPanel() {
  if (!collectionTasksBody) return;
  await loadCollectionTasks();
  const tasksToRefresh = collectionTasks.slice(0, 8).map(task => refreshCollectionTaskEvents(task.id));
  await Promise.all(tasksToRefresh);
  renderCollectionTasks();
}

function startCollectionTaskPolling() {
  if (collectionTaskPollingTimer) return;
  collectionTaskPollingTimer = setInterval(async () => {
    try {
      const beforeTotal = collectionPagination.total || 0;
      await refreshCollectionTaskPanel();
      const hasActiveCollectionTask = collectionTasks.some(task => ['queued', 'running'].includes(task.status));
      const latestTask = collectionTasks[0];
      const latestFinished = latestTask && !['queued', 'running'].includes(latestTask.status);
      if (hasActiveCollectionTask || latestFinished) {
        await loadCollectionItems({ resetPage: latestFinished && beforeTotal !== collectionPagination.total });
      }
    } catch (error) {
      console.warn('collection polling failed', error);
    }
  }, 3000);
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
  await refreshCollectionTaskPanel();
  await loadCollectionItems({ resetPage: true });
  addCollectionProgressLog('执行采集任务', ['completed', 'imported'].includes(task.status) ? 'success' : 'info', task.note || `采集任务状态：${collectionStatusText(task.status)}`);
  await notify(task.note || `采集任务状态：${collectionStatusText(task.status)}`);
}

async function cancelCollectionTask(taskId) {
  if (!await askConfirm('确认取消这个采集任务吗？队列中的任务会立即取消，运行中的任务会在当前步骤结束后停止。')) return;
  addCollectionProgressLog('取消采集任务', 'running', `正在取消任务 #${taskId}`);
  const response = await fetch(`/api/collection-tasks/${taskId}/cancel`, { method: 'POST' });
  if (!response.ok) {
    const error = await response.json();
    addCollectionProgressLog('取消采集任务', 'error', error.detail || '取消采集任务失败');
    await notify(error.detail || '取消采集任务失败');
    return;
  }
  const task = await response.json();
  await refreshCollectionTaskPanel();
  addCollectionProgressLog('取消采集任务', 'success', task.note || `采集任务状态：${collectionStatusText(task.status)}`);
  await notify(task.note || `采集任务状态：${collectionStatusText(task.status)}`);
}

async function waitForCollectionImportTask(taskId, selectedCount, progressLogs) {
  for (let index = 0; index < 360; index += 1) {
    const task = await fetchJson(`/api/collection-items/import-tasks/${taskId}`);
    const processed = task.processed_count || 0;
    const total = task.total_count || selectedCount;
    if (['completed', 'empty', 'failed'].includes(task.status)) return task;
    pushDialogProgress(progressLogs, '后台入库', 'running', `后台入库中：${processed}/${total}，新增 ${task.imported_count || 0} 条，跳过 ${task.skipped_count || 0} 条，失败 ${task.failed_count || 0} 条`);
    await new Promise(resolve => setTimeout(resolve, 1500));
  }
  throw new Error('入库任务仍在后台执行，请稍后刷新查看结果');
}

function normalizeCollectionBlacklist() {
  const input = byId('collectionBlacklist');
  if (!input) return '';
  const value = String(input.value || '').trim();
  if (/^(data|\.\/data|\\?data)[\\/].*\.json$/i.test(value)) {
    input.value = '';
    return '';
  }
  return value;
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
    blacklist: normalizeCollectionBlacklist(),
  };
}

async function watchCollectionTask(taskId, rounds = 8) {
  for (let index = 0; index < rounds; index += 1) {
    await refreshCollectionTaskPanel();
    await refreshCollectionTaskEvents(taskId);
    const events = collectionTaskEventsCache.get(Number(taskId)) || [];
    const latestEvent = events[events.length - 1];
    if (latestEvent) {
      const type = latestEvent.status === 'error' ? 'error' : (latestEvent.status === 'success' ? 'success' : 'info');
      addCollectionProgressLog(`\u4efb\u52a1 #${taskId}`, type, `${collectionEventStageText(latestEvent.stage)} \u00b7 ${cleanLogText(latestEvent.message || '')}`);
    }
    const task = collectionTasks.find(item => item.id === Number(taskId));
    if (task && !['queued', 'running'].includes(task.status)) {
      await loadCollectionItems({ resetPage: true });
      addCollectionProgressLog(`\u4efb\u52a1 #${taskId}`, task.status === 'failed' ? 'error' : 'success', `\u72b6\u6001\uff1a${collectionStatusText(task.status)}\uff1b\u65b0\u589e ${task.result_count || 0} \u6761`);
      return;
    }
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

async function startCollectionTask() {
  const payload = collectionTaskPayload();
  const batchHint = payload.target_count > 200 ? `\uff0c\u5c06\u6309\u6bcf\u6279 200 \u6761\u81ea\u52a8\u62c6\u5206` : '';
  addCollectionProgressLog('\u5f00\u59cb\u91c7\u96c6', 'running', `\u5df2\u63d0\u4ea4\u5173\u952e\u8bcd\u300c${payload.keyword || '-'}\u300d\u7684\u91c7\u96c6\u8bf7\u6c42${batchHint}\uff0c\u4efb\u52a1\u4f1a\u8fdb\u5165\u961f\u5217\u540e\u53f0\u6267\u884c`);
  const response = await fetch('/api/collection-tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json();
    addCollectionProgressLog('\u5f00\u59cb\u91c7\u96c6', 'error', error.detail || '\u521b\u5efa\u91c7\u96c6\u4efb\u52a1\u5931\u8d25');
    await notify(error.detail || '\u521b\u5efa\u91c7\u96c6\u4efb\u52a1\u5931\u8d25');
    return;
  }
  const task = await response.json();
  addCollectionProgressLog('\u5f00\u59cb\u91c7\u96c6', 'success', `\u4efb\u52a1 #${task.id} \u5df2\u8fdb\u5165\u961f\u5217\uff0c\u5f53\u524d\u72b6\u6001\uff1a${collectionStatusText(task.status)}${task.batch_total > 1 ? `\uff0c\u6279\u6b21 ${task.batch_index}/${task.batch_total}` : ''}`);
  await refreshCollectionTaskPanel();
  watchCollectionTask(task.id);
}


async function importCollectionFile(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  const data = new FormData();
  data.append('source', '外部文件');
  data.append('file', file);
  const response = await fetch('/api/collection-items/import-file', { method: 'POST', body: data });
  event.target.value = '';
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '导入采集文件失败');
    return;
  }
  const result = await response.json();
  await loadCollectionItems({ resetPage: true });
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

async function applyDefaultProcessingFieldsToNewItems(previousProductIds, progressLogs = [], importedProductIds = []) {
  await loadProcessingItems();
  const previous = new Set(previousProductIds || []);
  const explicitIds = (importedProductIds || []).map(Number).filter(Boolean);
  const newIds = explicitIds.length ? explicitIds : processingItems.map(item => item.product_id).filter(id => !previous.has(id));
  if (!newIds.length) return null;
  const fields = defaultProcessingFieldsPayload();
  const startSkc = byId('defaultProcessingStartSkc')?.value.trim() || '';
  pushDialogProgress(progressLogs, '批量字段设置', 'running', `正在给 ${newIds.length} 个新商品自动套用批量字段设置...`);
  const response = await fetch('/api/processing-items/field-tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids: newIds, fields, start_skc: startSkc }),
  });
  if (!response.ok) {
    const error = await response.json();
    pushDialogProgress(progressLogs, '批量字段设置', 'error', error.detail || '自动套用批量字段设置失败');
    return null;
  }
  const createdTask = await response.json();
  const task = await waitForProcessingFieldTask(createdTask.id);
  const type = task.failed_count ? 'error' : 'success';
  pushDialogProgress(progressLogs, '批量字段设置', type, task.note || `已自动套用 ${newIds.length} 个新商品`);
  await loadProcessingItems();
  return task;
}

async function importSelectedCollectionItems() {
  const ids = selectedCollectionIds();
  if (!ids.length) {
    await notify('请选择要加入商品库的采集结果');
    return;
  }
  const selectedItems = collectionItems.filter(item => ids.includes(item.id));
  const selectedCount = ids.length;
  const missingImageItems = selectedItems.filter(item => !item.image_url);
  const previewLines = selectedItems.slice(0, 6).map((item, index) => `${index + 1}. ${item.title || '未命名商品'}`);
  const moreText = selectedCount > previewLines.length ? `\n另外还有 ${selectedCount - previewLines.length} 条（可能在其他页）` : '';
  const missingText = missingImageItems.length ? `\n\n其中 ${missingImageItems.length} 条没有主图，建议先补图，否则进入商品处理后仍会显示需补图。` : '';
  const confirmed = await askConfirm(
    `确认将 ${selectedCount} 条采集结果加入商品库？\n\n${previewLines.join('\n')}${moreText}${missingText}`,
    '加入商品库确认'
  );
  if (!confirmed) return;
  const previousProductIds = processingItems.map(item => item.product_id);
  const progressLogs = [];
  const progressTitle = '加入商品库';
  openProgressDialog({ title: progressTitle, message: `正在创建后台入库任务：0/${selectedCount}...` });
  pushDialogProgress(progressLogs, '创建入库任务', 'running', `正在创建后台入库任务：0/${selectedCount}...`);
  const response = await fetch('/api/collection-items/import-tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  if (!response.ok) {
    const error = await response.json();
    pushDialogProgress(progressLogs, '入库失败', 'error', error.detail || '创建入库任务失败，点击完成关闭。');
    return;
  }
  const task = await response.json();
  pushDialogProgress(progressLogs, '后台入库', 'running', `入库任务 #${task.id} 已创建，后台开始处理 ${selectedCount} 条商品...`);
  let finishedTask;
  try {
    finishedTask = await waitForCollectionImportTask(task.id, selectedCount, progressLogs);
  } catch (error) {
    pushDialogProgress(progressLogs, '后台入库', 'error', error.message || '入库任务查询失败，点击完成关闭。');
    return;
  }
  pushDialogProgress(progressLogs, '刷新采集结果', 'running', '正在刷新页面数据...');
  ids.forEach(id => selectedCollectionIdsSet.delete(id));
  await loadCollectionItems();
  await loadProducts();
  await applyDefaultProcessingFieldsToNewItems(previousProductIds, progressLogs, finishedTask.imported_product_ids || []);
  loadUploadTasks();
  loadPublishRecords();
  const type = finishedTask.status === 'completed' ? 'success' : (finishedTask.failed_count ? 'error' : 'info');
  pushDialogProgress(progressLogs, '入库完成', type, displayTaskNote(finishedTask.note) || `已完成入库：新增 ${finishedTask.imported_count || 0} 条，跳过 ${finishedTask.skipped_count || 0} 条，失败 ${finishedTask.failed_count || 0} 条，点击完成关闭。`);
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
  ids.forEach(id => selectedCollectionIdsSet.delete(id));
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
    if (slot) clearManualDetailImageAssignment(slot.dataset.productId, slot.dataset.slotIndex, slot.dataset.imageUrl || '');
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
  const editFieldsButton = event.target.closest('[data-edit-processing-fields]');
  if (editFieldsButton) {
    event.preventDefault();
    const productId = Number(editFieldsButton.dataset.editProcessingFields);
    const item = processingItems.find(current => current.product_id === productId);
    if (item) openProcessingForm(item);
    return;
  }
  const fixTitleButton = event.target.closest('[data-fix-processing-title]');
  if (fixTitleButton) {
    event.preventDefault();
    generateTitleForProduct(fixTitleButton.dataset.fixProcessingTitle).then(() => loadProcessingItems());
    return;
  }
  const focusImagesButton = event.target.closest('[data-focus-processing-images]');
  if (focusImagesButton) {
    event.preventDefault();
    const target = processingDetailPanel.querySelector('.skc-manager') || processingDetailPanel.querySelector('.carousel-image-list');
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    return;
  }
  const specMappingButton = event.target.closest('[data-open-spec-mapping]');
  if (specMappingButton) {
    event.preventDefault();
    document.querySelector('[data-page="spec-mapping"]')?.click();
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
  const action = processingBatchAction?.value || '';
  if (!action) return;
  if (processingBatchAction) processingBatchAction.value = '';
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
  await refreshProcessingItem(productId);
}

function updateProcessingItemInMemory(productId, patch) {
  const id = Number(productId);
  const index = processingItems.findIndex(item => Number(item.product_id) === id);
  if (index < 0) return null;
  processingItems[index] = { ...processingItems[index], ...patch };
  return processingItems[index];
}

function renderUpdatedProcessingItem(productId) {
  renderProcessingItems();
  const item = processingItems.find(current => Number(current.product_id) === Number(productId));
  if (item && Number(selectedProcessingProductId) === Number(productId)) renderProcessingDetail(item);
}

async function detailImageAssignmentRequest(response, fallbackMessage, productId) {
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
  const assignments = await response.json();
  updateProcessingItemInMemory(productId, { detail_image_assignments: assignments || [] });
  renderUpdatedProcessingItem(productId);
  return true;
}

async function saveManualDetailImageAssignment(productId, slotIndex, imageUrl) {
  const response = await fetch('/api/processing-items/detail-image-assignment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), slot_index: Number(slotIndex), image_url: imageUrl || '' }),
  });
  return detailImageAssignmentRequest(response, '保存详情图失败', productId);
}

async function clearManualDetailImageAssignment(productId, slotIndex, imageUrl = '') {
  const item = processingItems.find(current => current.product_id === Number(productId));
  const detailAssignments = item?.detail_image_assignments || [];
  const sourceOptions = detailAssignments.length ? detailAssignments : uniqueImageOptionsByUrl((item?.image_options || []).filter(option => option.kind === 'detail_desc_image'));
  const remainingImageUrls = sourceOptions
    .map(option => option.image_url || option.url || '')
    .filter(url => url && url !== imageUrl);
  const fallbackResponse = await fetch('/api/processing-items/detail-image-assignment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), slot_index: Number(slotIndex), image_url: '', remove_image_url: imageUrl || '', remaining_image_urls: remainingImageUrls }),
  });
  return detailImageAssignmentRequest(fallbackResponse, '删除详情图失败', productId);
}

async function clearManualDetailImageAssignmentLegacy(productId, slotIndex) {
  const response = await fetch(`/api/processing-items/${Number(productId)}/detail-images/${Number(slotIndex)}`, { method: 'DELETE' });
  if (response.status !== 404 && response.status !== 405) return detailImageAssignmentRequest(response, '删除详情图失败', productId);
  const fallbackResponse = await fetch('/api/processing-items/detail-image-assignment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: Number(productId), slot_index: Number(slotIndex), image_url: '' }),
  });
  return detailImageAssignmentRequest(fallbackResponse, '删除详情图失败', productId);
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
  const assignments = await response.json();
  updateProcessingItemInMemory(productId, { color_image_assignments: assignments || [] });
  renderUpdatedProcessingItem(productId);
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
    await refreshProcessingItem(productId);
    await notify(`已生成英文标题：
${item.english_title}`);
  }
  addOperationLog('AI生成标题', 'success', `已生成标题：${item.english_title}`, Math.max(operationProgress, 60));
  return item;
}

async function waitForProcessingTitleTask(taskId) {
  for (let index = 0; index < 720; index += 1) {
    const task = await fetchJson(`/api/processing-items/title-tasks/${taskId}`);
    const processed = task.processed_count || 0;
    const total = task.total_count || 0;
    addOperationLog('批量生成标题', 'running', `标题任务 #${taskId}：${processed}/${total}，成功 ${task.success_count || 0}，失败 ${task.failed_count || 0}，缓存 ${task.cache_hit_count || 0}`, Math.min(75, 35 + Math.round((processed / Math.max(total, 1)) * 40)));
    if (['completed', 'failed'].includes(task.status)) return task;
    await new Promise(resolve => setTimeout(resolve, 1500));
  }
  throw new Error('标题任务仍在后台执行，请稍后刷新查看结果');
}

async function batchGenerateProcessingTitles() {
  const ids = selectedProcessingProductIds();
  if (!ids.length) {
    await notify('\u8bf7\u5148\u9009\u62e9\u8981\u5904\u7406\u6807\u9898\u7684\u5546\u54c1');
    return;
  }
  if (!await askConfirm(`\u786e\u8ba4\u6279\u91cf\u5904\u7406 ${ids.length} \u4e2a\u5546\u54c1\u6807\u9898\u5417\uff1f\n\n\u4f1a\u8fdb\u5165\u540e\u53f0\u961f\u5217\uff0c\u4f18\u5148\u547d\u4e2d\u7f13\u5b58\uff0c\u5bf9\u5f02\u5e38\u6807\u9898\u505a\u62e6\u622a\u8bb0\u5f55\u3002`)) return;
  addOperationLog('\u6279\u91cf\u751f\u6210\u6807\u9898', 'running', `\u6b63\u5728\u521b\u5efa ${ids.length} \u4e2a\u5546\u54c1\u7684\u6807\u9898\u5904\u7406\u4efb\u52a1`, 35);
  const response = await fetch('/api/processing-items/title-tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  if (!response.ok) {
    const error = await response.json();
    addOperationLog('\u6279\u91cf\u751f\u6210\u6807\u9898', 'error', error.detail || '\u6279\u91cf\u751f\u6210\u6807\u9898\u5931\u8d25', 35);
    await notify(error.detail || '\u6279\u91cf\u751f\u6210\u6807\u9898\u5931\u8d25');
    return;
  }
  const createdTask = await response.json();
  let task;
  try {
    task = await waitForProcessingTitleTask(createdTask.id);
  } catch (error) {
    addOperationLog('\u6279\u91cf\u751f\u6210\u6807\u9898', 'error', error.message || '\u6807\u9898\u4efb\u52a1\u67e5\u8be2\u5931\u8d25', 45);
    await notify(error.message || '\u6807\u9898\u4efb\u52a1\u67e5\u8be2\u5931\u8d25');
    return;
  }
  await loadProcessingItems();
  const type = task.failed_count ? 'error' : 'success';
  addOperationLog('\u6279\u91cf\u751f\u6210\u6807\u9898', type, task.note || `\u6210\u529f ${task.success_count || 0} \u4e2a\uff0c\u5931\u8d25 ${task.failed_count || 0} \u4e2a\uff0c\u547d\u4e2d\u7f13\u5b58 ${task.cache_hit_count || 0} \u4e2a`, 85);
  await notify(task.note || `\u6279\u91cf\u6807\u9898\u5904\u7406\u5b8c\u6210\uff1a\u6210\u529f ${task.success_count || 0} \u4e2a\uff0c\u5931\u8d25 ${task.failed_count || 0} \u4e2a\uff0c\u547d\u4e2d\u7f13\u5b58 ${task.cache_hit_count || 0} \u4e2a`);
}


async function waitForProcessingFieldTask(taskId) {
  for (let index = 0; index < 360; index += 1) {
    const task = await fetchJson(`/api/processing-items/field-tasks/${taskId}`);
    const processed = task.processed_count || 0;
    const total = task.total_count || 0;
    addOperationLog('批量字段处理', 'running', `字段任务 #${taskId}：${processed}/${total}，成功 ${task.success_count || 0}，失败 ${task.failed_count || 0}`, Math.min(80, 30 + Math.round((processed / Math.max(total, 1)) * 50)));
    if (['completed', 'failed'].includes(task.status)) return task;
    await new Promise(resolve => setTimeout(resolve, 1200));
  }
  throw new Error('批量字段任务仍在后台执行，请稍后刷新查看结果');
}

processingForm?.addEventListener('submit', async event => {
  event.preventDefault();
  const payload = processingPayload();
  const productId = byId('processingProductId').value;
  const isBulk = processingFormMode === 'bulk';
  const startSkc = isBulk ? byId('processingSourceUrl').value.trim() : '';
  if (isBulk) {
    const ids = productId.split(',').map(Number).filter(Boolean);
    addOperationLog('批量字段处理', 'running', `正在创建 ${ids.length} 个商品的批量字段任务`, 30);
    const response = await fetch('/api/processing-items/field-tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids, fields: payload, start_skc: startSkc }),
    });
    if (!response.ok) {
      const error = await response.json();
      await notify(error.detail || '创建批量字段任务失败');
      return;
    }
    closeProcessingForm();
    const createdTask = await response.json();
    let task;
    try {
      task = await waitForProcessingFieldTask(createdTask.id);
    } catch (error) {
      addOperationLog('批量字段处理', 'error', error.message || '批量字段任务查询失败', 40);
      await notify(error.message || '批量字段任务查询失败');
      return;
    }
    await refreshOperationalViews();
    addOperationLog('批量字段处理', task.failed_count ? 'error' : 'success', task.note || `成功 ${task.success_count || 0} 个，失败 ${task.failed_count || 0} 个`, 85);
    await notify(task.note || '批量字段保存完成');
    return;
  }
  const response = await fetch(`/api/processing-items/${productId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const error = await response.json();
    await notify(error.detail || '保存处理字段失败');
    return;
  }
  closeProcessingForm();
  await refreshProcessingItem(productId);
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

searchButton?.addEventListener('click', loadProducts);
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
function resetProcessingPageAndRender() {
  processingPagination.page = 1;
  loadProcessingItems();
}
processingStatusFilter?.addEventListener('change', resetProcessingPageAndRender);
processingSearchInput?.addEventListener('input', resetProcessingPageAndRender);
processingSearchInput?.addEventListener('keydown', event => { if (event.key === 'Enter') resetProcessingPageAndRender(); });
processingExceptionTypeFilter?.addEventListener('change', resetProcessingPageAndRender);
processingPageSize?.addEventListener('change', resetProcessingPageAndRender);
processingPrevPage?.addEventListener('click', () => {
  if (processingPagination.page <= 1) return;
  processingPagination.page -= 1;
  loadProcessingItems();
});
processingNextPage?.addEventListener('click', () => {
  if (processingPagination.page >= processingPagination.total_pages) return;
  processingPagination.page += 1;
  loadProcessingItems();
});
processingTaskCenterBody?.addEventListener('click', event => {
  const retryButton = event.target.closest('[data-processing-task-retry]');
  if (retryButton) retryProcessingTaskFailed(retryButton.dataset.processingTaskRetry);
});
processingTaskTypeFilter?.addEventListener('change', () => loadProcessingTaskCenter({ page: 1 }));
processingTaskStatusFilter?.addEventListener('change', () => loadProcessingTaskCenter({ page: 1 }));
refreshProcessingTasksButton?.addEventListener('click', () => loadProcessingTaskCenter());
processingTaskCenterPrev?.addEventListener('click', () => loadProcessingTaskCenter({ page: Math.max(1, (processingTaskCenter.page || 1) - 1) }));
processingTaskCenterNext?.addEventListener('click', () => loadProcessingTaskCenter({ page: Math.min(processingTaskCenter.total_pages || 1, (processingTaskCenter.page || 1) + 1) }));
if (selectAllProcessing) selectAllProcessing.addEventListener('change', () => {
  const visibleIds = pagedProcessingItems().map(item => item.product_id);
  if (selectAllProcessing.checked) visibleIds.forEach(id => selectedProcessingIds.add(id));
  else visibleIds.forEach(id => selectedProcessingIds.delete(id));
  renderProcessingItems();
});
processingBatchAction?.addEventListener('change', runProcessingBatchAction);
processingFieldSettingsButton?.addEventListener('click', event => {
  event.stopPropagation();
  processingFieldSettingsPanel?.classList.toggle('hidden');
});
processingFieldSettingsPanel?.addEventListener('click', event => event.stopPropagation());
document.addEventListener('click', () => processingFieldSettingsPanel?.classList.add('hidden'));
saveProcessingFieldSettingsButton?.addEventListener('click', async () => {
  await saveSettings({ silent: true });
  processingFieldSettingsPanel?.classList.add('hidden');
  await notify('批量字段设置已保存，后续采集结果进入商品处理会自动套用');
});
if (saveUploadOperationSettingsButton) saveUploadOperationSettingsButton.addEventListener('click', saveSettings);
if (createUploadTaskButton) createUploadTaskButton.addEventListener('click', realUpload);
if (createUploadTaskInlineButton) createUploadTaskInlineButton.addEventListener('click', createUploadTask);
if (clearUploadTasksButton) clearUploadTasksButton.addEventListener('click', clearUploadTasks);
if (cleanupLocalDataButton) cleanupLocalDataButton.addEventListener('click', cleanupLocalData);
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
if (retryFailedButton) retryFailedButton.addEventListener('click', retryFailedUpload);
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

freightImportFile?.addEventListener('change', async event => {
  try {
    await importFreightFile(event.target.files?.[0]);
  } catch (error) {
    await notify(error.message || '导入运费表失败');
  } finally {
    event.target.value = '';
  }
});
saveFreightRulesButton?.addEventListener('click', async () => {
  try {
    await saveFreightRules();
  } catch (error) {
    await notify(error.message || '保存运费模板失败');
  }
});
addFirstMileRuleButton?.addEventListener('click', () => {
  const current = collectFreightRules().first_mile;
  current.push({ channel: '空运', max_weight_g: 10000000, price_per_kg: 69, fixed_fee: 4 });
  renderFirstMileEditor(current);
});
addLastMileRuleButton?.addEventListener('click', () => {
  const current = collectFreightRules().last_mile;
  current.push({ channel: 'Temu', max_weight_g: 0, zones: {} });
  renderLastMileEditor(current);
});
firstMileRuleEditor?.addEventListener('click', event => {
  if (!event.target.closest('[data-remove-freight-row]')) return;
  event.target.closest('.freight-rule-row')?.remove();
});
lastMileRuleEditor?.addEventListener('click', event => {
  if (!event.target.closest('[data-remove-freight-row]')) return;
  event.target.closest('.freight-rule-row')?.remove();
});
refreshFreightRulesButton?.addEventListener('click', loadFreightRules);
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
      const id = Number(input.dataset.collectionId);
      if (!id) return;
      if (selectAllCollection.checked) selectedCollectionIdsSet.add(id);
      else selectedCollectionIdsSet.delete(id);
    });
    renderCollectionPagination();
  });
}
collectionBody?.addEventListener('change', event => {
  const input = event.target.closest('[data-collection-id]');
  if (!input) return;
  const id = Number(input.dataset.collectionId);
  if (!id) return;
  if (input.checked) selectedCollectionIdsSet.add(id);
  else selectedCollectionIdsSet.delete(id);
  syncCollectionSelectAllState();
  renderCollectionPagination();
});
byId('collectionSearchInput')?.addEventListener('keydown', event => { if (event.key === 'Enter') loadCollectionItems({ resetPage: true }); });
if (importSelectedButton) importSelectedButton.addEventListener('click', importSelectedCollectionItems);
if (deleteSelectedCollectionButton) deleteSelectedCollectionButton.addEventListener('click', () => updateSelectedCollectionItems('delete'));
selectFilteredCollectionButton?.addEventListener('click', selectFilteredCollectionItems);
clearCollectionSelectionButton?.addEventListener('click', clearCollectionSelection);
if (applyCollectionFiltersButton) applyCollectionFiltersButton.addEventListener('click', () => loadCollectionItems({ resetPage: true }));
collectionPrevPageButton?.addEventListener('click', () => {
  if ((collectionPagination.page || 1) <= 1) return;
  collectionPagination.page -= 1;
  loadCollectionItems();
});
collectionNextPageButton?.addEventListener('click', () => {
  if ((collectionPagination.page || 1) >= (collectionPagination.total_pages || 1)) return;
  collectionPagination.page += 1;
  loadCollectionItems();
});
collectionPageSizeSelect?.addEventListener('change', () => {
  collectionPagination.page_size = Number(collectionPageSizeSelect.value || 50);
  loadCollectionItems({ resetPage: true });
});
refreshSpecMappingsButton?.addEventListener('click', () => loadSpecMappings(true));
specAliasKind?.addEventListener('change', renderSpecAliasTargets);
saveSpecAliasButton?.addEventListener('click', saveSpecAlias);
specExceptionList?.addEventListener('click', event => {
  const button = event.target.closest('[data-spec-exception-bind]');
  if (button) bindSpecException(button.dataset.specExceptionBind);
});
specAliasSavedList?.addEventListener('click', event => {
  const button = event.target.closest('[data-spec-alias-delete]');
  if (button) deleteSpecAlias(button.dataset.specAliasDelete);
});
if (startCollectionTaskButton) startCollectionTaskButton.addEventListener('click', startCollectionTask);
if (clearCollectionTasksButton) clearCollectionTasksButton.addEventListener('click', clearCollectionTasks);
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
  if (event.target.dataset.collectionCancel) cancelCollectionTask(event.target.dataset.collectionCancel);
  if (event.target.dataset.collectionEvents) openCollectionTaskEvents(event.target.dataset.collectionEvents);
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

normalizeCollectionBlacklist();
refreshOperationalViews();
loadCollectionItems();
loadCollectionTasks();
startCollectionTaskPolling();
loadApiConfigs();
loadSettings();
loadSystemStatus();
loadPrompts();
loadProcessingTaskCenter();
runPreflight();
