
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.compare-btn');
  if (!btn) return;

  const url = btn.dataset.compareUrl;
  if (!url) return;

  const csrftoken = getCookie('csrftoken');

  // feedback immédiat
  btn.disabled = true;
  const oldText = btn.textContent;
  btn.textContent = 'Ajout...';

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken, 'X-Requested-With': 'XMLHttpRequest',},
    });

    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();

    if (data && data.ok) {
      btn.classList.remove('btn-outline-primary');
      btn.classList.add('btn-secondary');
      btn.textContent = 'Ajouté';
    } else {
      throw new Error('Réponse invalide');
    }
  } catch (err) {
    console.error(err);
    btn.disabled = false;
    btn.textContent = oldText;
    alert("Impossible d'ajouter au comparateur pour le moment.");
  }
});
