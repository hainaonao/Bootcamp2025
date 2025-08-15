// Dữ liệu y hệt trong file page.tsx
const tags = ["Toán", "Vật lý", "Hóa học", "Khoa học", "Các hoạt động STEM"];
const featuredVideos = [
  {
    id: 1,
    title: "Toán học lớp 3",
    thumbnail: "/static/img/bg1.png",
    duration: "12:34",
    views: "125K",
    likes: "3.2K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán",
  },
  {
    id: 2,
    title: "Khoa học lớp 3",
    thumbnail: "/static/img/bg1.png",
    duration: "8:45",
    views: "89K",
    likes: "2.1K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Khoa học",
  },
  {
    id: 3,
    title: "Khoa học lớp 4",
    thumbnail: "/static/img/bg1.png",
    duration: "15:22",
    views: "234K",
    likes: "5.7K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Khoa học",
  },
  {
    id: 4,
    title: "Khoa học lớp 5",
    thumbnail: "/static/img/bg1.png",
    duration: "10:18",
    views: "156K",
    likes: "4.3K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán",
  },
  {
    id: 5,
    title: "Toán lớp 5",
    thumbnail: "/static/img/bg1.png",
    duration: "18:56",
    views: "198K",
    likes: "6.1K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán",
  },
  {
    id: 6,
    title: "Toán lớp 3",
    thumbnail: "/static/img/bg1.png",
    duration: "14:33",
    views: "167K",
    likes: "4.8K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán",
  },
];

document.addEventListener("DOMContentLoaded", () => {
  // Render tags
  const tagsContainer = document.getElementById("tags");
  tags.forEach((tag) => {
    const el = document.createElement("span");
    el.textContent = tag;
    el.className = "px-4 py-2 bg-gray-200 rounded-full text-sm hover:bg-gray-300 cursor-pointer";
    tagsContainer.appendChild(el);
  });

  // Render featured videos
  const grid = document.getElementById("video-grid");
  featuredVideos.forEach((video) => {
    const card = document.createElement("a");
    card.href = "VideoSingle.html";
    card.className = "bg-white rounded-lg overflow-hidden shadow group hover:shadow-lg transition";

    card.innerHTML = `
      <div class="relative">
        <img src="${video.thumbnail}" alt="${video.title}"
             class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
        <div class="absolute bottom-2 right-2 bg-black bg-opacity-80 text-white px-2 py-1 text-sm rounded">
          ${video.duration}
        </div>
        <div class="absolute top-3 left-3 bg-orange-500 text-white font-bold px-3 py-1 rounded-full text-sm inline-block z-10">
          ${video.category}
        </div>
      </div>
      <div class="p-4">
        <h3 class="font-semibold text-gray-900 mb-2 group-hover:text-orange-600 transition-colors">${video.title}</h3>
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center space-x-2">
            <img src="${video.author.avatar}" alt="${video.author.name}"
                 class="w-6 h-6 rounded-full object-cover">
            <span class="text-sm text-gray-600">${video.author.name}</span>
          </div>
          <button class="p-1 hover:bg-gray-100 rounded-full focus:outline-none">
            <i data-lucide="more-horizontal" class="w-4 h-4"></i>
          </button>
        </div>
        <div class="flex items-center justify-between text-sm text-gray-500">
          <span>${video.views} lượt xem</span>
          <div class="flex items-center space-x-1">
            <i data-lucide="heart" class="w-4 h-4"></i>
            <span>${video.likes}</span>
          </div>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
});

// Toggle mobile menu
document.addEventListener("DOMContentLoaded", function() {
  const btn = document.getElementById("mobile-menu-btn");
  const menu = document.getElementById("mobile-menu");
  if (btn && menu) {
    btn.addEventListener("click", () => {
      menu.classList.toggle("hidden");
    });
  }
});
//Search



// Avatar dropdown + Notification dropdown
document.addEventListener("DOMContentLoaded", function () {
  const bellBtn   = document.getElementById("bell-btn");
  const bellDrop  = document.getElementById("notification-dropdown");
  const avatarBtn = document.getElementById("avatar-btn");
  const avatarMenu= document.getElementById("avatar-menu");

  const hide   = el => { if (el && !el.classList.contains("hidden")) el.classList.add("hidden"); };
  const toggle = el => { if (el) el.classList.toggle("hidden"); };

  document.addEventListener("click", function (e) {
    // Click chuông
    if (bellBtn && bellBtn.contains(e.target)) {
      e.stopPropagation();
      toggle(bellDrop);
      hide(avatarMenu);
      return;
    }
    // Click avatar
    if (avatarBtn && avatarBtn.contains(e.target)) {
      e.stopPropagation();
      toggle(avatarMenu);
      hide(bellDrop);
      return;
    }
    // Click ra ngoài -> đóng cả hai
    if (!bellDrop || !bellDrop.contains(e.target)) hide(bellDrop);
    if (!avatarMenu || !avatarMenu.contains(e.target)) hide(avatarMenu);
  });

  // Nhấn ESC -> đóng cả hai
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      hide(bellDrop);
      hide(avatarMenu);
    }
  });
});
