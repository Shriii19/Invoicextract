const API = 'http://localhost:8000';

// ── State ─────────────────────────────────────────────────────────────────
let currentFile = null;
let lastResult = null;

// ── Element refs ──────────────────────────────────────────────────────────
const dropZone     = document.getElementById('dropZone');
const fileInput    = document.getElementById('fileInput');
const fileSelected = document.getElementById('fileSelected');
const fileName     = document.getElementById('fileName');
const clearBtn     = document.getElementById('clearBtn');
const extractBtn   = document.getElementById('extractBtn');
const btnText      = document.getElementById('btnText');
const btnSpinner   = document.getElementById('btnSpinner');
const errorBox     = document.getElementById('errorBox');
const uploadSection  = document.getElementById('uploadSection');
const resultsSection = document.getElementById('resultsSection');
const newBtn       = document.getElementById('newBtn');

// ── File selection ────────────────────────────────────────────────────────
fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

clearBtn.addEventListener('click', () => clearFile());

function setFile(file) {
  currentFile = file;
  fileName.textContent = file.name;
  fileSelected.classList.remove('hidden');
  extractBtn.disabled = false;
  hideError();
}

function clearFile() {
  currentFile = null;
  fileInput.value = '';
  fileSelected.classList.add('hidden');
  extractBtn.disabled = true;
  hideError();
}

// ── Drag & Drop ───────────────────────────────────────────────────────────
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
});
dropZone.addEventListener('click', e => {
  if (e.target.closest('label')) return;
  fileInput.click();
});

// ── Extract ───────────────────────────────────────────────────────────────
extractBtn.addEventListener('click', async () => {
  if (!currentFile) return;
  setLoading(true);
  hideError();

  try {
    const form = new FormData();
    form.append('file', currentFile);

    const res = await fetch(`${API}/api/extract`, { method: 'POST', body: form });
    const data = await res.json();

    if (!res.ok) {
      showError(data.detail || `Server error ${res.status}`);
      return;
    }

    lastResult = data;
    renderResults(data);
    uploadSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
  } catch (err) {
    showError('Could not reach the backend. Make sure the server is running on port 8000.');
  } finally {
    setLoading(false);
  }
});

// ── New invoice ───────────────────────────────────────────────────────────
newBtn.addEventListener('click', () => {
  resultsSection.classList.add('hidden');
  uploadSection.classList.remove('hidden');
  clearFile();
  lastResult = null;
});

// ── Downloads ─────────────────────────────────────────────────────────────
document.getElementById('dlCsv').addEventListener('click',   () => download('csv'));
document.getElementById('dlExcel').addEventListener('click', () => download('excel'));
document.getElementById('dlJson').addEventListener('click',  () => download('json'));

async function download(format) {
  if (!currentFile) return;
  const form = new FormData();
  form.append('file', currentFile);
  form.append('format', format);

  const res = await fetch(`${API}/api/extract/download`, { method: 'POST', body: form });
  if (!res.ok) { showError('Download failed.'); return; }

  const blob = await res.blob();
  const ext = format === 'excel' ? 'xlsx' : format;
  const url = URL.createObjectURL(blob);
  const a   = document.createElement('a');
  a.href = url;
  a.download = `invoice.${ext}`;
  a.click();
  URL.revokeObjectURL(url);
}

// ── Render results ────────────────────────────────────────────────────────
function renderResults(data) {
  const inv = data.invoice;
  const fmt = (n, cur) => n != null ? `${cur || ''} ${Number(n).toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2})}`.trim() : '—';

  // Header
  document.getElementById('invoiceNum').textContent = inv.invoice_number ? `Invoice #${inv.invoice_number}` : 'Invoice';
  const badge = document.getElementById('validBadge');
  badge.textContent = inv.is_valid ? 'Valid' : 'Invalid';
  badge.className = `badge ${inv.is_valid ? 'valid' : 'invalid'}`;
  document.getElementById('extractedTime').textContent = inv.extracted_at
    ? `Extracted ${new Date(inv.extracted_at).toLocaleString()}` : '';

  // Dates
  set('invoiceDate', inv.dates.invoice_date || '—');
  set('dueDate',     inv.dates.due_date     || '—');

  // Vendor
  set('vendorName',    inv.vendor.name    || '—');
  set('vendorEmail',   inv.vendor.email   || '');
  set('vendorPhone',   inv.vendor.phone   || '');
  set('vendorAddress', formatAddress(inv.vendor.address));

  // Customer
  set('customerName',    inv.customer.name    || '—');
  set('customerAddress', formatAddress(inv.customer.address));

  // Amounts
  const cur = inv.amounts.currency || '';
  set('subtotal',   fmt(inv.amounts.subtotal, cur));
  set('taxAmount',  fmt(inv.amounts.tax,      cur));
  set('totalAmount', fmt(inv.amounts.total,   cur));

  // Payment terms
  const payRow = document.getElementById('paymentRow');
  if (inv.payment_terms) {
    set('paymentTerms', inv.payment_terms);
    payRow.classList.remove('hidden');
  } else {
    payRow.classList.add('hidden');
  }

  // Line items
  const tbody = document.getElementById('lineItemsBody');
  tbody.innerHTML = '';
  if (inv.line_items && inv.line_items.length > 0) {
    inv.line_items.forEach((item, i) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${i + 1}</td>
        <td>${esc(item.description)}</td>
        <td class="right">${item.quantity != null ? item.quantity : '—'}</td>
        <td class="right">${item.unit_price != null ? fmt(item.unit_price, cur) : '—'}</td>
        <td class="right">${item.amount != null ? fmt(item.amount, cur) : '—'}</td>`;
      tbody.appendChild(tr);
    });
  } else {
    tbody.innerHTML = '<tr><td colspan="5" class="no-items">No line items detected</td></tr>';
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────
function set(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function esc(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function formatAddress(addr) {
  if (!addr) return '';
  // Remove leading name line if it duplicates vendor/customer name already shown
  return addr;
}

function setLoading(on) {
  extractBtn.disabled = on;
  btnText.classList.toggle('hidden', on);
  btnSpinner.classList.toggle('hidden', !on);
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove('hidden');
}

function hideError() {
  errorBox.classList.add('hidden');
  errorBox.textContent = '';
}
