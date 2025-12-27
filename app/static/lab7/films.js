document.addEventListener('DOMContentLoaded', () => { initAddFilmForm(); });

function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function(data) {
            return data.json();
        })
        .then(function(films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');
                
                tdTitle.innerText = films[i].title;
                tdTitleRus.innerText = films[i].title_ru;
                tdYear.innerText = films[i].year;
                
                let editBtn = document.createElement('button');
                editBtn.innerText = 'Редактировать';
                editBtn.className = 'btn';
                editBtn.style.cssText = 'margin-right: 10px !important;';
                editBtn.onclick = function() { editFilm(i); };
                
                let delBtn = document.createElement('button');
                delBtn.innerText = 'Удалить';
                delBtn.className = 'btn btn-danger';
                delBtn.onclick = function() { deleteFilm(i); };
                
                tdActions.appendChild(editBtn);
                tdActions.appendChild(delBtn);
                
                tr.appendChild(tdTitle);
                tr.appendChild(tdTitleRus);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);
                
                tbody.appendChild(tr);
            }
        });
}

function escapeHtml(s) {
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// -------- Инициализация формы добавления --------
function initAddFilmForm() {
    const openBtn = document.getElementById('add-film-btn');
    const modal = document.getElementById('add-film-modal');
    const cancelBtn = document.getElementById('add-film-cancel');
    const submitBtn = document.getElementById('add-film-submit');

    openBtn && openBtn.addEventListener('click', () => openAddForm());
    cancelBtn && cancelBtn.addEventListener('click', (e) => { e.preventDefault(); closeAddForm(); });
    submitBtn && submitBtn.addEventListener('click', (e) => { e.preventDefault(); submitAddForm(); });

    // Закрытие по клику вне контента
    modal && modal.addEventListener('click', (e) => {
        if (e.target === modal) closeAddForm();
    });
}

function openAddForm() {
    const modal = document.getElementById('add-film-modal');
    const errorBox = document.getElementById('add-film-error');
    if (!modal) return;
    // если задан id, переключим заголовок на редактирование
    const idEl = document.getElementById('film-id');
    const titleEl = document.getElementById('modal-title');
    if (idEl && idEl.value) {
        titleEl && (titleEl.innerText = 'Редактировать фильм');
    } else {
        titleEl && (titleEl.innerText = 'Добавить фильм');
    }
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
    errorBox && (errorBox.style.display = 'none');
}

function closeAddForm() {
    const modal = document.getElementById('add-film-modal');
    if (!modal) return;
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
    // очистка полей
    document.getElementById('film-title').value = '';
    document.getElementById('film-title-ru').value = '';
    document.getElementById('film-year').value = '2020';
    document.getElementById('film-description').value = '';
    // очистить id и заголовок
    const idEl = document.getElementById('film-id');
    if (idEl) idEl.value = '';
    const titleEl = document.getElementById('modal-title');
    titleEl && (titleEl.innerText = 'Добавить фильм');
}

async function submitAddForm() {
    const idEl = document.getElementById('film-id');
    const id = idEl ? idEl.value : '';

    const titleEl = document.getElementById('film-title');
    const titleRuEl = document.getElementById('film-title-ru');
    const yearEl = document.getElementById('film-year');
    const descEl = document.getElementById('film-description');
    const errorBox = document.getElementById('add-film-error');

    const title = titleEl.value.trim();
    const title_ru = (titleRuEl.value.trim() || title);
    const year = parseInt(yearEl.value, 10);
    const description = descEl.value.trim();

    // простая валидация
    if (!title) {
        showFormError('Поле "Название" обязательно');
        return;
    }
    if (!Number.isInteger(year) || year < 1800 || year > 2100) {
        showFormError('Введите корректный год');
        return;
    }

    const payload = { title, title_ru, year, description };

    try {
        const url = id ? ('/lab7/rest-api/films/' + id) : '/lab7/rest-api/films/';
        const method = id ? 'PUT' : 'POST';

        const res = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            showFormError(data.error || 'Ошибка ' + res.status);
            return;
        }

        // очистим id при успешном сохранении
        if (idEl) idEl.value = '';
        closeAddForm();
        fillFilmList();
    } catch (err) {
        console.error('Ошибка при сохранении фильма:', err);
        showFormError('Ошибка при сохранении фильма');
    }
}

// Редактирование фильма
async function editFilm(id) {
    try {
        const res = await fetch('/lab7/rest-api/films/' + id);
        if (!res.ok) {
            alert('Не удалось получить данные фильма');
            return;
        }
        const film = await res.json();
        document.getElementById('film-id').value = id;
        document.getElementById('film-title').value = film.title || '';
        document.getElementById('film-title-ru').value = film.title_ru || film.title || '';
        document.getElementById('film-year').value = film.year || '2020';
        document.getElementById('film-description').value = film.description || '';
        openAddForm();
    } catch (err) {
        console.error('Ошибка при загрузке фильма:', err);
        alert('Ошибка при загрузке фильма');
    }
}

function showFormError(msg) {
    const errorBox = document.getElementById('add-film-error');
    if (!errorBox) return;
    errorBox.textContent = msg;
    errorBox.style.display = 'block';
}

async function deleteFilm(id) {
    if (!confirm('Удалить фильм?')) return;
    try {
        const res = await fetch('/lab7/rest-api/films/' + id, { method: 'DELETE' });
        if (res.status === 204) {
            fillFilmList();
        } else {
            alert('Ошибка удаления');
        }
    } catch (err) {
        console.error('Ошибка при удалении:', err);
        alert('Ошибка при удалении');
    }
}

// Экспорт функций при необходимости
window.deleteFilm = deleteFilm;