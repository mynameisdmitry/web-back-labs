document.addEventListener('DOMContentLoaded', loadFilms);

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
                <td style="padding:10px;"><button class="btn btn-danger" onclick="deleteFilm(${i})">Удалить</button></td>
            `;
            list.appendChild(tr);
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

async function addFilm() {
    const title = prompt('Название (оригинал):');
    if (!title) return;
    const title_ru = prompt('Название (на русском):') || title;
    const yearStr = prompt('Год:', '2020');
    const description = prompt('Описание:', '');
    const year = parseInt(yearStr, 10) || 2020;

    const payload = { title, title_ru, year, description };

    try {
        const res = await fetch('/lab7/rest-api/films/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            alert('Ошибка: ' + (data.error || res.status));
            return;
        }

        loadFilms();
    } catch (err) {
        console.error('Ошибка при добавлении фильма:', err);
        alert('Ошибка при добавлении фильма');
    }
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

// Экспорт в глобальную область, чтобы inline onclick работал
window.addFilm = addFilm;
window.deleteFilm = deleteFilm;