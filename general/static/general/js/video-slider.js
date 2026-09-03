const videoTexts = window.VIDEO_TEXTS || [
    "Promouvoir une Côte d'Ivoire connectée, Hub de l'Afrique Moderne !",
    "Le génie ivoirien à l'œuvre d'une nouvelle ère !",
    "La science des données au cœur de l'Intelligence Economique !"
];
const videos = [
    { src: "/static/general/videos/video1.mp4", text: videoTexts[0] },
    { src: "/static/general/videos/video2.mp4", text: videoTexts[1] },
    { src: "/static/general/videos/video3.mp4", text: videoTexts[2] }
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
        if (i <= htmlText.length) {
            textEl.innerHTML = htmlText.slice(0, i);
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