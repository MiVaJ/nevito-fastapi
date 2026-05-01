const API_URL = "/api/messages";

// Универсальное уведомление с цветовой индикацией
function notify(text, type = "success") {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`; 
    toast.textContent = text;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.5s ease';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// Загрузка сообщений
async function loadMessages() {
    try {
        const response = await fetch(API_URL);
        const messages = await response.json();
        const container = document.getElementById('messagesContainer');
        
        container.innerHTML = messages.map(msg => `
            <div class="message-item">
                <div class="message-info"><p>${msg.content}</p></div>
                <div class="message-actions">
                    <button onclick="prepareEdit(${msg.id}, '${msg.content.replace(/'/g, "\\'")}')" class="btn btn-secondary">Редактировать</button>
                    <button onclick="deleteMessage(${msg.id})" class="btn btn-delete">Удалить</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        notify("Ошибка загрузки данных", "danger");
    }
}

// Сохранение сообщений
async function saveMessage() {
    const id = document.getElementById('editId').value;
    const content = document.getElementById('messageInput').value.trim();

    if (!content) {
        notify("Текст не может быть пустым", "danger");
        return;
    }

    const isEdit = id !== '';
    const method = isEdit ? 'PUT' : 'POST';
    const url = isEdit ? `${API_URL}/${id}` : API_URL;

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: content })
        });

        if (response.ok) {
            // Зеленый для создания, оранжевый для обновления
            notify(isEdit ? "Сообщение обновлено" : "Сообщение создано", isEdit ? "warning" : "success");
            resetForm();
            await loadMessages();
        }
    } catch (error) {
        notify("Ошибка сети", "danger");
    }
}

// Удаление сообщений
async function deleteMessage(id) {
    if (!confirm('Удалить сообщение?')) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        if (response.ok) {
            notify("Сообщение удалено", "danger"); // Красный для удаления
            await loadMessages();
        }
    } catch (error) {
        notify("Сбой при удалении", "danger");
    }
}

// Подготовка страницы к редактировани
function prepareEdit(id, content) {
    document.getElementById('editId').value = id;
    document.getElementById('messageInput').value = content;
    document.getElementById('formTitle').textContent = 'Редактирование #' + id;
    document.getElementById('sendBtn').textContent = 'Сохранить изменения';
    document.getElementById('cancelBtn').style.display = 'inline-block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Обновление формы
function resetForm() {
    document.getElementById('editId').value = '';
    document.getElementById('messageInput').value = '';
    document.getElementById('formTitle').textContent = 'Новое сообщение';
    document.getElementById('sendBtn').textContent = 'Опубликовать';
    document.getElementById('cancelBtn').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', loadMessages);