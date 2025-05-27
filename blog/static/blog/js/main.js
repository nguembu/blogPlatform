document.addEventListener('DOMContentLoaded', function() {
    // --- Messages flash ---
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // --- Animation + AJAX like ---
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            // Animation
            this.classList.add('animate__animated', 'animate__heartBeat');
            setTimeout(() => {
                this.classList.remove('animate__animated', 'animate__heartBeat');
            }, 1000);

            // Données
            const postId = this.getAttribute('data-post-id');
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Requête AJAX
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
            })
            .then(response => response.json())
            .then(data => {
                // Met à jour le compteur et l’icône
                const likeCountSpan = this.querySelector('#like-count');
                if (likeCountSpan) {
                    likeCountSpan.textContent = data.likes_count;
                }
                if (data.liked) {
                    this.innerHTML = `<i class="fas fa-heart"></i> <span id="like-count">${data.likes_count}</span>`;
                    this.classList.remove('btn-outline-primary');
                    this.classList.add('btn-primary');
                } else {
                    this.innerHTML = `<i class="far fa-heart"></i> <span id="like-count">${data.likes_count}</span>`;
                    this.classList.remove('btn-primary');
                    this.classList.add('btn-outline-primary');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // --- Simulation chargement posts ---
    const loadMoreButton = document.getElementById('load-more');
    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', function() {
            const newPosts = document.createElement('div');
            newPosts.classList.add('post');
            newPosts.innerHTML = `
                <img src="path_to_new_image.jpg" class="post-image" alt="Nouvelle publication">
                <h3>Nouveau Post</h3>
                <p>Contenu du nouveau post...</p>
            `;
            document.querySelector('.posts-container').appendChild(newPosts);
            this.style.display = 'none';
        });
    }

    // --- Scroll fluide ---
    const scrollLinks = document.querySelectorAll('a.scroll-to');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
});
