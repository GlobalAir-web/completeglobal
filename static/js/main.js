document.addEventListener("DOMContentLoaded", () => {

/* ================= SAFE GSAP CHECK ================= */
const HAS_GSAP = typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined";
if (HAS_GSAP) gsap.registerPlugin(ScrollTrigger);

const IS_HOME = document.body.classList.contains("home-page");

/* ================= NAV DROPDOWN (MOBILE) ================= */
const dropBtn = document.querySelector(".dropbtn");
const dropdown = document.querySelector(".dropdown-menu");

if (dropBtn && dropdown) {
  dropBtn.addEventListener("click", (e) => {
    if (window.innerWidth < 768) {
      e.preventDefault();
      e.stopPropagation();
      dropdown.style.display =
        dropdown.style.display === "flex" ? "none" : "flex";
    }
  });
}

/* ================= BACKGROUND DRIFT ================= */
window.addEventListener("scroll", ()=>{
  const offset = window.scrollY * 0.04;
  document.body.style.backgroundPosition = `center ${-offset}px`;
});

/* ===== HARD NAVBAR SCROLL CONTROLLER ===== */
window.addEventListener("load", function () {
  const navbar = document.querySelector(".navbar");
  if (!navbar) return;
  let lastY = window.scrollY;
  const backBtn = document.querySelector(".back-btn, a[href='/home'][style*='fixed']");
  const isMobile = window.innerWidth < 768;

  window.addEventListener("scroll", function () {
    const y = window.scrollY;
    if (y > lastY && y > 140) {
      navbar.classList.add("nav-hidden");
      // On mobile, keep back button visible; on desktop, hide it
      if (backBtn && !isMobile) backBtn.style.opacity = "0";
    } else {
      navbar.classList.remove("nav-hidden");
      if (backBtn) backBtn.style.opacity = "1";
    }
    lastY = y;
  }, { passive: true });
});

/* ================= HERO VIDEO AUTOPLAY ================= */
window.addEventListener("load", () => {
  const heroVideo = document.querySelector(".hero video");
  if(heroVideo){
    heroVideo.muted = true;
    heroVideo.play().catch(()=>{});
  }
});

/* ================= MOBILE MENU ================= */
const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

if (menuToggle && navLinks) {
  /* Toggle on hamburger click */
  menuToggle.addEventListener("click", function(e) {
    e.stopPropagation();
    e.preventDefault();
    navLinks.classList.toggle("active");
  });

  /* Close when clicking outside */
  document.addEventListener("click", function(e) {
    if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
      navLinks.classList.remove("active");
    }
  });

  /* Close when a link is clicked */
  navLinks.querySelectorAll("a").forEach(function(link) {
    link.addEventListener("click", function() {
      navLinks.classList.remove("active");
    });
  });
}

/* ===================================== */
/* PRODUCT SLIDER + FLIP — FINAL STABLE  */
/* ===================================== */

(function(){

  const slider = document.getElementById("slider");
  if (!slider) return;

  const viewport = slider.closest(".slider-viewport");
  const cards    = slider.querySelectorAll(".product-card");
  if (!cards.length) return;

  let index = 0;

  function gap() {
    return parseFloat(getComputedStyle(slider).gap) || 24;
  }

  function cardWidth() {
    return cards[0].offsetWidth + gap();
  }

  function visibleCount() {
    return Math.max(1, Math.floor(viewport.offsetWidth / cardWidth()));
  }

  function maxIndex() {
    return Math.max(0, cards.length - visibleCount());
  }

  function updateSlider() {
    slider.style.transform = `translateX(-${index * cardWidth()}px)`;
    document.querySelectorAll(".slider-side-btn.left")
      .forEach(b => b.disabled = index === 0);
    document.querySelectorAll(".slider-side-btn.right")
      .forEach(b => b.disabled = index >= maxIndex());
  }

  window.slidePage = function(dir) {
    index += dir;
    if (index < 0) index = 0;
    if (index > maxIndex()) index = maxIndex();
    updateSlider();
  };

  window.addEventListener("resize", () => {
    index = 0;
    updateSlider();
  });

  /* touch swipe */
  let startX = 0;
  if (viewport) {
    viewport.addEventListener("touchstart", e => {
      startX = e.touches[0].clientX;
    }, { passive: true });
    viewport.addEventListener("touchend", e => {
      const diff = startX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) {
        window.slidePage(diff > 0 ? 1 : -1);
      }
    });
  }

  updateSlider();

  /* ================= FLIP LOGIC ================= */
  const flipCards = slider.querySelectorAll(".has-flip");

  flipCards.forEach(card => {
    card.addEventListener("click", e => {
      if (e.target.closest("a")) return;
      e.stopPropagation();
      flipCards.forEach(c => { if (c !== card) c.classList.remove("flipped"); });
      card.classList.toggle("flipped");
    });
  });

  document.addEventListener("click", e => {
    if (!e.target.closest(".has-flip")) {
      flipCards.forEach(c => c.classList.remove("flipped"));
    }
  });

})();

/* ===== CERT SLIDER ===== */
(function(){
  const slider = document.getElementById("certSlider");
  if (!slider) return;
  const cards = slider.querySelectorAll(".cert-card");
  if (!cards.length) return;
  let index = 0;

  function step(){
    const gap = parseFloat(getComputedStyle(slider).gap) || 28;
    return cards[0].offsetWidth + gap;
  }
  function visible(){
    return Math.floor(slider.parentElement.offsetWidth / step());
  }
  function maxIndex(){
    return Math.max(0, cards.length - visible());
  }
  function update(){
    slider.style.transform = `translateX(-${index * step()}px)`;
    document.querySelectorAll(".cert-side-btn.left")
      .forEach(b => b.disabled = index === 0);
    document.querySelectorAll(".cert-side-btn.right")
      .forEach(b => b.disabled = index >= maxIndex());
  }

  window.moveCert = function(dir){
    index += dir;
    if (index < 0) index = 0;
    if (index > maxIndex()) index = maxIndex();
    update();
  };

  window.addEventListener("resize", update);
  update();
})();

/* ================= CERTIFICATE MODAL ================= */
const certModal = document.getElementById("certModal");
const certModalImg = document.getElementById("certModalImg");

window.openCertModal = function(card){
  if (!certModal || !certModalImg) return;
  const img = card.querySelector("img");
  if (!img) return;
  certModalImg.src = img.src;
  certModal.classList.add("active");
  document.body.style.overflow = "hidden";
};

window.closeCertModal = function(){
  if (!certModal) return;
  certModal.classList.remove("active");
  document.body.style.overflow = "";
};

window.modalNext = function(){};
window.modalPrev = function(){};

/* ================= CONTACT FORM ================= */
window.submitContactForm = function(e){
  e.preventDefault();
  fetch("/submit_contact",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({
      name:e.target.name.value,
      email:e.target.email.value,
      phone:e.target.countryCode.value + " " + e.target.phone.value,
      subject:e.target.subject.value,
      message:e.target.message.value
    })
  })
  .then(r=>r.json())
  .then(d=>{
    alert(d.status==="success" ? "Message sent!" : "Error!");
    if(d.status==="success") e.target.reset();
  })
  .catch(()=>alert("Server error"));
};

/* ================= GALLERY SLIDER ================= */
(function(){
  const slider = document.getElementById("gallerySlider");
  if (!slider) return;
  const viewport = slider.closest(".gallery-viewport");
  if (!viewport) return;
  let idx = 0;

  function imgWidth() {
    const img = slider.querySelector("img");
    const gap = parseFloat(getComputedStyle(slider).gap) || 28;
    return img ? img.offsetWidth + gap : 0;
  }

  function visibleCount() {
    const iw = imgWidth();
    return iw > 0 ? Math.max(1, Math.floor(viewport.offsetWidth / iw)) : 1;
  }

  function maxIdx() {
    return Math.max(0, slider.querySelectorAll("img").length - visibleCount());
  }

  window.moveGallery = function(dir) {
    idx += dir;
    if (idx < 0) idx = 0;
    if (idx > maxIdx()) idx = maxIdx();
    slider.style.transform = "translateX(-" + (idx * imgWidth()) + "px)";
  };

  window.addEventListener("resize", function() {
    idx = 0;
    slider.style.transform = "translateX(0)";
  });

  let startX = 0;
  viewport.addEventListener("touchstart", function(e) {
    startX = e.touches[0].clientX;
  }, { passive: true });
  viewport.addEventListener("touchend", function(e) {
    const diff = startX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) window.moveGallery(diff > 0 ? 1 : -1);
  });
})();

/* ================= GALLERY MODAL ================= */
function openGalleryModal(img){
  const modal = document.getElementById("galleryModal");
  const modalImg = document.getElementById("galleryModalImg");
  if (!modal || !modalImg) return;
  modalImg.src = img.src;
  modal.classList.add("active");
}

function closeGallery(){
  const modal = document.getElementById("galleryModal");
  if (modal) modal.classList.remove("active");
}

/* ================= AWARDS SLIDER ================= */
let awardsIndex = 0;

function moveAwards(direction){
  const slider = document.getElementById("awardsSlider");
  if(!slider) return;
  const images = slider.querySelectorAll("img");
  const visible = 2;
  const maxIdx = images.length - visible;
  awardsIndex += direction * visible;
  if(awardsIndex < 0) awardsIndex = 0;
  if(awardsIndex > maxIdx) awardsIndex = maxIdx;
  slider.style.transform = `translateX(-${awardsIndex * 50}%)`;
}

/* ===== LOCATION PAGE REVEAL ===== */
if (document.querySelector(".location-page") && HAS_GSAP) {
  gsap.to(".loc-title", { opacity:1, y:0, duration:1.2, ease:"power3.out" });
  gsap.to(".loc-sub",   { opacity:1, y:0, duration:1.2, delay:0.2, ease:"power3.out" });
  gsap.from(".map-box", { opacity:0, y:40, duration:1.3, delay:0.35, ease:"power3.out" });
}

/* ===== CONTACT DETAILS REVEAL ===== */
if (HAS_GSAP && document.querySelector(".contact-details-block")) {
  gsap.to(".detail-item", {
    scrollTrigger: { trigger:".contact-details-block", start:"top 80%", once:true },
    opacity:1, y:0, duration:0.8, stagger:0.25, ease:"power3.out"
  });
}

/* ================= GSAP ANIMATIONS ================= */
if (HAS_GSAP && IS_HOME) {
  gsap.to(".navbar",{opacity:1,y:0,duration:1});
  gsap.to(".logo-container img, .logo-container span",
    {opacity:1,y:0,stagger:.15,duration:.8,delay:.3});
  gsap.fromTo(".nav-links a",
    {opacity:0,y:10},
    {opacity:1,y:0,stagger:.08,duration:.6,delay:.6});
  gsap.to(".team-card",{
    scrollTrigger:{trigger:"#team",start:"top 80%",once:true},
    opacity:1,y:0,stagger:.2
  });
  ScrollTrigger.create({
    trigger:"#why-us",
    start:"top 85%",
    once:true,
    onEnter:()=> gsap.to("#why-us .video-mask",
      {opacity:1,y:0,scale:1,duration:1.4})
  });
}

/* ===== IMAGE MODAL ===== */
function openImageModal(src) {
  const modal = document.getElementById("imageModal");
  const img   = document.getElementById("modalImage");
  if (!modal || !img) return;
  img.src = src;
  modal.classList.add("show");
  document.body.style.overflow = "hidden";
}

function closeImageModal() {
  const modal = document.getElementById("imageModal");
  if (modal) modal.classList.remove("show");
  document.body.style.overflow = "auto";
}

document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") closeImageModal();
});

});