// ==== DỮ LIỆU VIDEO: bạn có thể lấy trực tiếp từ API hoặc json bên dưới ====
const allVideos = [
  {
    id: 1,
    title: "Toán học lớp 3",
    thumbnail: "/static/img/bg1.png",
    duration: "12:34",
    views: "125K",
    likes: "3.2K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán"
  },
  {
    id: 2,
    title: "Khoa học lớp 3",
    thumbnail: "/static/img/bg1.png",
    duration: "8:45",
    views: "89K",
    likes: "2.1K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpgg" },
    category: "Khoa học"
  },
  {
    id: 3,
    title: "Khoa học lớp 4",
    thumbnail: "/static/img/bg1.png",
    duration: "15:22",
    views: "234K",
    likes: "5.7K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Khoa học"
  },
  {
    id: 4,
    title: "Khoa học lớp 5",
    thumbnail: "/static/img/bg1.png",
    duration: "10:18",
    views: "156K",
    likes: "4.3K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán"
  },
  {
    id: 5,
    title: "Toán lớp 5",
    thumbnail: "/static/img/bg1.png",
    duration: "18:56",
    views: "198K",
    likes: "6.1K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán"
  },
  {
    id: 6,
    title: "Toán lớp 3",
    thumbnail: "/static/img/bg1.png",
    duration: "14:33",
    views: "167K",
    likes: "4.8K",
    author: { name: "Tiến Nguyễn", avatar: "/static/img/au1.jpg" },
    category: "Toán"
  }
  // ... (Bạn bổ sung thêm video nếu có)
];

function renderVideos(videos) {
  const grid = document.getElementById("all-videos-grid");
  grid.innerHTML = "";
  videos.forEach((video) => {
    const card = document.createElement("div");
    card.className = "bg-white rounded-lg overflow-hidden shadow group hover:shadow-lg transition cursor-pointer";
    card.onclick = () => {
      window.location.href = "VideoSingle.html"; // hoặc truyền id nếu muốn
    };
    card.innerHTML = `
      <div class="relative">
        <img src="${video.thumbnail}" alt="${video.title}" class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
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
            <img src="${video.author.avatar}" alt="${video.author.name}" class="w-6 h-6 rounded-full object-cover">
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
  lucide.createIcons();
}

// Tìm kiếm video
document.addEventListener("DOMContentLoaded", function () {
  renderVideos(allVideos);

  const search = document.getElementById("video-search");
  const category = document.getElementById("video-category");

  function filterVideos() {
    const searchQuery = search.value.trim().toLowerCase();
    const selectedCategory = category.value;
    
    const filtered = allVideos.filter(video => {
      const matchesSearch = video.title.toLowerCase().includes(searchQuery) || 
                            video.author.name.toLowerCase().includes(searchQuery) || 
                            video.category.toLowerCase().includes(searchQuery);

      const matchesCategory = selectedCategory === 'all' || video.category.toLowerCase() === selectedCategory;
      
      return matchesSearch && matchesCategory;
    });
    renderVideos(filtered);
  }

  // Lắng nghe sự kiện thay đổi bộ lọc
  category.addEventListener("change", filterVideos);

  // Lắng nghe sự kiện tìm kiếm
  search.addEventListener("input", filterVideos);
});


 const filterButton = document.getElementById('filter-button');
  const filterPopup = document.getElementById('filter-popup');

  // Mở popup khi nhấn vào nút bộ lọc
  filterButton.addEventListener('click', () => {
    filterPopup.classList.toggle('hidden');
  });

  // Đóng popup khi nhấn ngoài popup
  filterPopup.addEventListener('click', (e) => {
    if (e.target === filterPopup) {
      filterPopup.classList.add('hidden');
    }
  });

  // Cập nhật giá trị slider
  const durationSlider = document.getElementById('duration');
  const ratingSlider = document.getElementById('rating');
  const durationValue = document.getElementById('duration-value');
  const ratingValue = document.getElementById('rating-value');

  durationSlider.addEventListener('input', () => {
    durationValue.textContent = `${durationSlider.value} phút`;
  });

  ratingSlider.addEventListener('input', () => {
    ratingValue.textContent = `${ratingSlider.value} sao`;
  });