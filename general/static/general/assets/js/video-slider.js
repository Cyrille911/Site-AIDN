const videos = [
    {
        src: "{% static 'general/videos/video1.mp4' %}",
        text: "Bienvenue dans notre premier module vidéo<br>Découvrez les innovations numériques"
    },
    {
        src: "{% static 'general/videos/video2.mp4' %}",
        text: "Innovation & Performance<br>au cœur de l'État"
    },
    {
        src: "{% static 'general/videos/video3.mp4' %}",
        text: "Données & Décision<br>pour le Développement"
    }
];

let currentIndex = 0;
const videoEl = document.getElementById("video-slider");
const textEl = document.getElementById("video-text");

// Préchargement des vidéos
const preloadVideos = videos.map(video => {
    const vid = document.createElement("video");
    vid.src = video.src;
    vid.muted = true;
    vid.playsInline = true;
    return vid;
});

// Fonction d'animation texte lettre par lettre
function typeText(htmlText, speed = 50) {
    textEl.innerHTML = "";
    let i = 0;
    const type = () => {
        if (i < htmlText.length) {
            textEl.innerHTML += htmlText.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    };
    type();
}

// Chargement de la vidéo suivante avec fade
function loadNextVideo() {
    currentIndex = (currentIndex + 1) % videos.length;

    // Fade out
    videoEl.classList.remove("active");

    setTimeout(() => {
        videoEl.src = videos[currentIndex].src;
        videoEl.load();
        videoEl.play();
        videoEl.classList.add("active");

        // Animation du texte correspondant
        typeText(videos[currentIndex].text);
    }, 1000); // correspond à la durée de la transition CSS
}

// Écouter la fin de la vidéo courante
videoEl.addEventListener("ended", loadNextVideo);

// Démarrage initial
videoEl.src = videos[0].src;
videoEl.classList.add("active");
typeText(videos[0].text);