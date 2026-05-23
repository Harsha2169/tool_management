// ===== Configuration =====
const API_BASE = "http://localhost:8000/api/v1";

// ===== State =====
let currentPage = 0;
const pageSize = 20;
let totalTools = 0;
let currentToolId = null; // tool_id of currently selected tool (for edit)
let isEditMode = false;

// ===== DOM Elements =====
const toolsTableBody = document.getElementById("toolsTableBody");
const tableEmpty = document.getElementById("tableEmpty");
const modalOverlay = document.getElementById("modalOverlay");
const searchInput = document.getElementById("searchInput");
const filterToolType = document.getElementById("filterToolType");
const filterStatus = document.getElementById("filterStatus");

// ===== Initialize =====
document.addEventListener("DOMContentLoaded", () => {
    loadToolTypes();
    loadTools();
    setupEventListeners();
});

// ===== Event Listeners =====
function setupEventListeners() {
    // Add New button
    document.getElementById("btnAddNew").addEventListener("click", () => openModal());

    // Close modal
    document.getElementById("btnCloseModal").addEventListener("click", closeModal);
    modalOverlay.addEventListener("click", (e) => {
        if (e.target === modalOverlay) closeModal();
    });

    // Cancel master form
    document.getElementById("btnCancelMaster").addEventListener("click", closeModal);

    // Master form submit
    document.getElementById("masterForm").addEventListener("submit", handleMasterSave);

    // Modal tabs
    document.querySelectorAll(".modal-tab").forEach(tab => {
        tab.addEventListener("click", () => switchModalTab(tab.dataset.modalTab));
    });

    // Page tabs
    document.querySelectorAll(".tab").forEach(tab => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
        });
    });

    // Search & Filters
    searchInput.addEventListener("input", debounce(loadTools, 400));
    filterToolType.addEventListener("change", loadTools);
    filterStatus.addEventListener("change", loadTools);

    // Pagination
    document.getElementById("btnPrev").addEventListener("click", () => { currentPage--; loadTools(); });
    document.getElementById("btnNext").addEventListener("click", () => { currentPage++; loadTools(); });

    // Production
    document.getElementById("btnAddProduction").addEventListener("click", () => toggleInlineForm("productionForm", true));
    document.getElementById("btnCancelProduction").addEventListener("click", () => toggleInlineForm("productionForm", false));
    document.getElementById("btnSaveProduction").addEventListener("click", saveProduction);

    // Performance
    document.getElementById("btnAddPerformance").addEventListener("click", () => toggleInlineForm("performanceForm", true));
    document.getElementById("btnCancelPerformance").addEventListener("click", () => toggleInlineForm("performanceForm", false));
    document.getElementById("btnSavePerformance").addEventListener("click", savePerformance);

    // Params
    document.getElementById("btnAddParam").addEventListener("click", () => toggleInlineForm("paramsForm", true));
    document.getElementById("btnCancelParam").addEventListener("click", () => toggleInlineForm("paramsForm", false));
    document.getElementById("btnSaveParam").addEventListener("click", saveParam);

    // Maintenance
    document.getElementById("btnAddMaintenance").addEventListener("click", () => toggleInlineForm("maintenanceForm", true));
    document.getElementById("btnCancelMaintenance").addEventListener("click", () => toggleInlineForm("maintenanceForm", false));
    document.getElementById("btnSaveMaintenance").addEventListener("click", saveMaintenance);
}

// ===== API Helpers =====
async function apiFetch(url, options = {}) {
    try {
        const res = await fetch(url, {
            headers: { "Content-Type": "application/json" },
            ...options
        });
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || `HTTP ${res.status}`);
        }
        if (res.status === 204) return null;
        return await res.json();
    } catch (e) {
        console.error("API Error:", e);
        alert("Error: " + e.message);
        throw e;
    }
}

// ===== Load Tool Types (for filter & form) =====
async function loadToolTypes() {
    try {
        const types = await apiFetch(`${API_BASE}/lookups/tool-types`);
        const options = types.map(t => `<option value="${t.id}" data-name="${escapeHtml(t.name)}">${escapeHtml(t.name)}</option>`).join("");

        document.getElementById("fToolType").innerHTML = `<option value="">Select Type</option>` + options;
        filterToolType.innerHTML = `<option value="">All Types</option>` + types.map(t => `<option value="${escapeHtml(t.name)}">${escapeHtml(t.name)}</option>`).join("");
    } catch (e) {
        
    }
}

// ===== Load Tools =====
async function loadTools() {
    const search = searchInput.value.trim();
    const toolType = filterToolType.value;
    const status = filterStatus.value;

    let url = `${API_BASE}/tools?skip=${currentPage * pageSize}&limit=${pageSize}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;
    if (toolType) url += `&tool_type=${encodeURIComponent(toolType)}`;
    if (status) url += `&life_status=${encodeURIComponent(status)}`;

    try {
        const data = await apiFetch(url);
        totalTools = data.total;
        renderToolsTable(data.items);
        updatePagination();
    } catch (e) {
        // Show empty state if API not available
        toolsTableBody.innerHTML = "";
        tableEmpty.style.display = "block";
    }
}

// ===== Render Tools Table =====
function renderToolsTable(items) {
    if (!items || items.length === 0) {
        toolsTableBody.innerHTML = "";
        tableEmpty.style.display = "block";
        return;
    }

    tableEmpty.style.display = "none";
    toolsTableBody.innerHTML = items.map(tool => {
        const usage = tool.usage_percentage || 0;
        let usageClass = "usage-low";
        if (usage >= 80) usageClass = "usage-high";
        else if (usage >= 50) usageClass = "usage-medium";

        return `
            <tr data-tool-id="${escapeHtml(tool.tool_id)}" onclick="openToolDetail('${escapeHtml(tool.tool_id)}')">
                <td><a class="tool-id-link">${escapeHtml(tool.tool_id)}</a></td>
                <td>${escapeHtml(tool.tool_description)}</td>
                <td>${escapeHtml(tool.tool_type_name || '')}</td>
                <td>${Number(tool.lifecycle_limit).toLocaleString()}</td>
                <td><span class="usage-badge ${usageClass}">${usage}%</span></td>
            </tr>
        `;
    }).join("");
}

// ===== Pagination =====
function updatePagination() {
    const totalPages = Math.ceil(totalTools / pageSize);
    document.getElementById("pageInfo").textContent = `Page ${currentPage + 1} of ${totalPages || 1}`;
    document.getElementById("btnPrev").disabled = currentPage <= 0;
    document.getElementById("btnNext").disabled = currentPage >= totalPages - 1;
}

// ===== Modal =====
function openModal(toolId = null) {
    currentToolId = toolId;
    isEditMode = !!toolId;
    modalOverlay.classList.add("active");
    switchModalTab("master");

    if (isEditMode) {
        document.getElementById("fToolId").readOnly = true;
        document.getElementById("btnSaveMaster").textContent = "Update";
        loadToolDetail(toolId);
    } else {
        document.getElementById("fToolId").readOnly = false;
        document.getElementById("btnSaveMaster").textContent = "Save";
        resetMasterForm();
    }
}

function closeModal() {
    modalOverlay.classList.remove("active");
    currentToolId = null;
    isEditMode = false;
    resetMasterForm();
}

function switchModalTab(tabName) {
    document.querySelectorAll(".modal-tab").forEach(t => t.classList.toggle("active", t.dataset.modalTab === tabName));
    document.querySelectorAll(".modal-tab-content").forEach(c => c.classList.toggle("active", c.id === `tab-${tabName}`));

    // Load sub-data when switching tabs (only in edit mode)
    if (isEditMode && currentToolId) {
        if (tabName === "production") loadProductions();
        if (tabName === "performance") loadPerformances();
        if (tabName === "params") loadParams();
        if (tabName === "maintenance") loadMaintenances();
    }
}

// ===== Open Tool Detail =====
function openToolDetail(toolId) {
    openModal(toolId);
}

// ===== Load Tool Detail =====
async function loadToolDetail(toolId) {
    try {
        const tool = await apiFetch(`${API_BASE}/tools/${encodeURIComponent(toolId)}`);
        document.getElementById("fToolId").value = tool.tool_id;
        document.getElementById("fToolDesc").value = tool.tool_description;
        document.getElementById("fToolType").value = tool.tool_type_id;
        document.getElementById("fLifeStatus").value = tool.life_status;
        document.getElementById("fMake").value = tool.make || "";
        document.getElementById("fModel").value = tool.model || "";
        document.getElementById("fAssetOwner").value = tool.asset_owner;
        document.getElementById("fAcquiredDate").value = tool.acquired_date || "";
        document.getElementById("fLifecycleLimit").value = tool.lifecycle_limit;
        document.getElementById("fControlUnit").value = tool.control_unit;
        document.getElementById("fInitialValue").value = tool.lifecycle_initial_value || 0;
        document.getElementById("fPlantId").value = tool.plant_id || "";
    } catch (e) {
        // handled in apiFetch
    }
}

// ===== Save Master =====
async function handleMasterSave(e) {
    e.preventDefault();

    const payload = {
        tool_id: document.getElementById("fToolId").value.trim(),
        tool_description: document.getElementById("fToolDesc").value.trim(),
        tool_type_id: parseInt(document.getElementById("fToolType").value),
        life_status: document.getElementById("fLifeStatus").value,
        make: document.getElementById("fMake").value.trim() || null,
        model: document.getElementById("fModel").value.trim() || null,
        asset_owner: document.getElementById("fAssetOwner").value,
        acquired_date: document.getElementById("fAcquiredDate").value || null,
        lifecycle_limit: parseInt(document.getElementById("fLifecycleLimit").value),
        control_unit: document.getElementById("fControlUnit").value,
        lifecycle_initial_value: parseInt(document.getElementById("fInitialValue").value) || 0,
        plant_id: document.getElementById("fPlantId").value.trim() || null,
    };

    try {
        if (isEditMode) {
            await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}`, {
                method: "PUT",
                body: JSON.stringify(payload),
            });
            alert("Tool updated!");
        } else {
            await apiFetch(`${API_BASE}/tools`, {
                method: "POST",
                body: JSON.stringify(payload),
            });
            currentToolId = payload.tool_id;
            isEditMode = true;
            document.getElementById("fToolId").readOnly = true;
            document.getElementById("btnSaveMaster").textContent = "Update";
            alert("Tool created!");
        }
        // Clear filters so user can see the new/updated tool
        searchInput.value = "";
        filterToolType.value = "";
        filterStatus.value = "";
        currentPage = 0;
        loadTools();
    } catch (e) {
        // handled in apiFetch
    }
}

function resetMasterForm() {
    document.getElementById("masterForm").reset();
    document.getElementById("fLifeStatus").value = "Active";
    document.getElementById("fInitialValue").value = "0";
    // Clear sub-tables
    document.getElementById("productionTableBody").innerHTML = "";
    document.getElementById("performanceTableBody").innerHTML = "";
    document.getElementById("paramsCardList").innerHTML = "";
    document.getElementById("maintenanceTableBody").innerHTML = "";
}

// ===== Production CRUD =====
async function loadProductions() {
    if (!currentToolId) return;
    try {
        const items = await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/productions`);
        document.getElementById("productionTableBody").innerHTML = items.map(p => `
            <tr>
                <td>${escapeHtml(p.tool_part_code)}</td>
                <td>${p.cavities}</td>
                <td>${escapeHtml(p.cavity_numbers || '')}</td>
                <td>${p.weight_all_parts_g || ''}</td>
                <td>${p.weight_runner_g || ''}</td>
                <td>${p.weight_shot_g || ''}</td>
                <td>
                    <button class="btn-icon" onclick="deleteProduction(${p.id})" title="Delete">🗑️</button>
                </td>
            </tr>
        `).join("");
    } catch (e) { /* handled */ }
}

async function saveProduction() {
    const payload = {
        tool_part_code: document.getElementById("pPartCode").value.trim(),
        cavities: parseInt(document.getElementById("pCavities").value),
        cavity_numbers: document.getElementById("pCavityNums").value.trim() || null,
        weight_all_parts_g: parseFloat(document.getElementById("pWtParts").value) || null,
        weight_runner_g: parseFloat(document.getElementById("pWtRunner").value) || null,
        weight_shot_g: parseFloat(document.getElementById("pWtShot").value) || null,
    };
    if (!payload.tool_part_code || !payload.cavities) { alert("Part Code and Cavities are required"); return; }

    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/productions`, {
            method: "POST", body: JSON.stringify(payload)
        });
        toggleInlineForm("productionForm", false);
        loadProductions();
    } catch (e) { /* handled */ }
}

async function deleteProduction(id) {
    if (!confirm("Delete this production entry?")) return;
    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/productions/${id}`, { method: "DELETE" });
        loadProductions();
    } catch (e) { /* handled */ }
}

// ===== Performance CRUD =====
async function loadPerformances() {
    if (!currentToolId) return;
    try {
        const items = await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/performances`);
        document.getElementById("performanceTableBody").innerHTML = items.map(p => `
            <tr>
                <td>${p.start_date}</td>
                <td>${p.end_date || ''}</td>
                <td>${p.performance_value || ''}</td>
                <td>${p.cumulative || ''}</td>
                <td>${escapeHtml(p.uom)}</td>
                <td>
                    <button class="btn-icon" onclick="deletePerformance(${p.id})" title="Delete">🗑️</button>
                </td>
            </tr>
        `).join("");
    } catch (e) { /* handled */ }
}

async function savePerformance() {
    const startDate = document.getElementById("perfStartDate").value;
    if (!startDate) { alert("Start Date is required"); return; }

    const payload = {
        start_date: startDate,
        end_date: document.getElementById("perfEndDate").value || null,
        performance_value: parseFloat(document.getElementById("perfValue").value) || null,
        cumulative: parseFloat(document.getElementById("perfCumulative").value) || null,
        uom: document.getElementById("perfUom").value,
    };

    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/performances`, {
            method: "POST", body: JSON.stringify(payload)
        });
        toggleInlineForm("performanceForm", false);
        loadPerformances();
    } catch (e) { /* handled */ }
}

async function deletePerformance(id) {
    if (!confirm("Delete this performance record?")) return;
    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/performances/${id}`, { method: "DELETE" });
        loadPerformances();
    } catch (e) { /* handled */ }
}

// ===== Params CRUD =====
async function loadParams() {
    if (!currentToolId) return;
    try {
        const items = await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/params`);
        const ordinals = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth'];
        document.getElementById("paramsCardList").innerHTML = items.map((p, i) => `
            <div class="param-card">
                <div>
                    <div class="param-card-label">${ordinals[i] || (i+1) + 'th'} parameter</div>
                    <div class="param-card-value">${escapeHtml(p.parameter_name)}</div>
                </div>
                <div>
                    <div class="param-card-label">Parameter Value</div>
                    <div class="param-card-value">${escapeHtml(p.parameter_value)}</div>
                </div>
                <div>
                    <div class="param-card-label">UoM</div>
                    <div class="param-card-value">${escapeHtml(p.uom || '-')}</div>
                </div>
                <div>
                    <button class="btn-icon" onclick="deleteParam(${p.id})" title="Delete">🗑️</button>
                </div>
            </div>
        `).join("") || '<p style="color:#7F8C8D;font-size:13px;">No parameters added yet.</p>';
    } catch (e) { /* handled */ }
}

async function saveParam() {
    const name = document.getElementById("paramName").value.trim();
    const value = document.getElementById("paramValue").value.trim();
    if (!name || !value) { alert("Parameter Name and Value are required"); return; }

    const payload = {
        parameter_name: name,
        parameter_value: value,
        uom: document.getElementById("paramUom").value || null,
    };

    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/params`, {
            method: "POST", body: JSON.stringify(payload)
        });
        toggleInlineForm("paramsForm", false);
        loadParams();
    } catch (e) { /* handled */ }
}

async function deleteParam(id) {
    if (!confirm("Delete this parameter?")) return;
    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/params/${id}`, { method: "DELETE" });
        loadParams();
    } catch (e) { /* handled */ }
}

// ===== Maintenance CRUD =====
async function loadMaintenances() {
    if (!currentToolId) return;
    try {
        const items = await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/maintenances`);
        document.getElementById("maintenanceTableBody").innerHTML = items.map(m => `
            <tr>
                <td>${m.maintenance_date}</td>
                <td>${escapeHtml(m.maintenance_type || '')}</td>
                <td>${escapeHtml(m.description || '')}</td>
                <td>${escapeHtml(m.performed_by || '')}</td>
                <td>${m.next_due_date || ''}</td>
                <td>${m.cost || ''}</td>
                <td>
                    <button class="btn-icon" onclick="deleteMaintenance(${m.id})" title="Delete">🗑️</button>
                </td>
            </tr>
        `).join("");
    } catch (e) { /* handled */ }
}

async function saveMaintenance() {
    const maintDate = document.getElementById("maintDate").value;
    if (!maintDate) { alert("Maintenance Date is required"); return; }

    const payload = {
        maintenance_date: maintDate,
        maintenance_type: document.getElementById("maintType").value.trim() || null,
        description: document.getElementById("maintDesc").value.trim() || null,
        performed_by: document.getElementById("maintBy").value.trim() || null,
        next_due_date: document.getElementById("maintNextDue").value || null,
        cost: parseFloat(document.getElementById("maintCost").value) || null,
    };

    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/maintenances`, {
            method: "POST", body: JSON.stringify(payload)
        });
        toggleInlineForm("maintenanceForm", false);
        loadMaintenances();
    } catch (e) { /* handled */ }
}

async function deleteMaintenance(id) {
    if (!confirm("Delete this maintenance record?")) return;
    try {
        await apiFetch(`${API_BASE}/tools/${encodeURIComponent(currentToolId)}/maintenances/${id}`, { method: "DELETE" });
        loadMaintenances();
    } catch (e) { /* handled */ }
}

// ===== Utility =====
function toggleInlineForm(formId, show) {
    const el = document.getElementById(formId);
    // Handle both tfoot (table row) and div forms
    if (el.tagName === 'TFOOT') {
        el.style.display = show ? 'table-footer-group' : 'none';
    } else {
        el.style.display = show ? 'block' : 'none';
    }
    if (!show) {
        el.querySelectorAll("input").forEach(i => i.value = "");
        el.querySelectorAll("select").forEach(s => s.selectedIndex = 0);
    }
}

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function debounce(fn, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}
