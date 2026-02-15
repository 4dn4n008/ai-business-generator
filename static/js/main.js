document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('generator-form');
    if (!form) return;

    var overlay = document.getElementById('loading-overlay');
    var stepText = document.getElementById('loading-step');

    var steps = [
        'Analyse de ton profil...',
        'Recherche de la meilleure idee business...',
        'Creation du plan sur 30 jours...',
        'Redaction de la strategie marketing...',
        'Ecriture des scripts TikTok...',
        'Calcul des estimations de revenus...',
        'Preparation du plan de monetisation...',
        'Finalisation de ton plan business...'
    ];

    form.addEventListener('submit', function () {
        overlay.style.display = 'flex';

        var i = 0;
        setInterval(function () {
            i++;
            if (i < steps.length) {
                stepText.textContent = steps[i];
            }
        }, 5000);
    });
});
