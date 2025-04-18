// Fonction pour afficher les messages pendant 5 secondes puis les faire disparaître
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des messages flash
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Animation pour le bouton like
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('animate__animated', 'animate__heartBeat');
            setTimeout(() => {
                this.classList.remove('animate__animated', 'animate__heartBeat');
            }, 1000);
        });
    });

    // Fonction pour le chargement dynamique des posts
    const loadMoreButton = document.getElementById('load-more');
    if (loadMoreButton) {
        loadMoreButton.addEventListener('click', function() {
            // Simule le chargement de nouveaux posts
            const newPosts = document.createElement('div');
            newPosts.classList.add('post');
            newPosts.innerHTML = `
                <img src="path_to_new_image.jpg" class="post-image" alt="Nouvelle publication">
                <h3>Nouveau Post</h3>
                <p>Contenu du nouveau post...</p>
            `;
            document.querySelector('.posts-container').appendChild(newPosts);
            this.style.display = 'none'; // Cache le bouton après le chargement
        });
    }

    // Fonction pour le défilement fluide vers les sections
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