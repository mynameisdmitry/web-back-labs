document.addEventListener('DOMContentLoaded', () => { loadFilms(); initAddFilmForm(); });

async function loadFilms() {
    const list = document.getElementById('film-list');
    if (!list) return;

    try {
        const res = await fetch('/lab7/rest-api/films/');
        if (!res.ok) throw new Error('Network response was not ok');
        const films = await res.json();

        list.innerHTML = '';

        if (films.length === 0) {
            const tr = document.createElement('tr');
            tr.innerHTML = '<td colspan="4" style="padding:16px; text-align:center; color:#666;">Список пуст</td>';
            list.appendChild(tr);
            return;
        }

        films.forEach((f, i) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="width:80px; padding:10px;"><img src="/static/lab7/poster.svg" alt="poster" style="width:60px; height:auto; border-radius:6px;"></td>
                <td style="padding:10px;"><strong>${escapeHtml(f.title_ru)}</strong><div style="color:#666">${escapeHtml(f.title)}</div></td>
                <td style="padding:10px;">${escapeHtml(String(f.year))}</td>
                <td style="padding:10px;"><button class="btn btn-danger" data-id="${i}">Удалить</button></td>
            `;
            list.appendChild(tr);
        });

        // attach delete handlers
        document.querySelectorAll('#film-list .btn-danger').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = Number(btn.getAttribute('data-id'));
                deleteFilm(id);
            });
        });
    } catch (err) {
        console.error('Ошибка при загрузке фильмов:', err);
    }
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
}

async function submitAddForm() {
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
        const res = await fetch('/lab7/rest-api/films/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            showFormError(data.error || 'Ошибка ' + res.status);
            return;
        }

        closeAddForm();
        loadFilms();
    } catch (err) {
        console.error('Ошибка при добавлении фильма:', err);
        showFormError('Ошибка при добавлении фильма');
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
            loadFilms();
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