// Mock video data
const mockVideos = [
  {
    id: 1,
    title: "How to Build Modern Web Applications with Next.js",
    thumbnail: "/web-dev-tutorial-thumbnail.png",
    duration: "12:34",
    views: "1.2M",
    likes: "45K",
    publishedDate: "2 days ago",
    channel: {
      name: "TechTutorials",
      avatar: "/tech-channel-avatar.png",
      verified: true,
    },
    videoUrl: "/sample-video.mp4",
  },
  {
    id: 2,
    title: "React Hooks Explained: useState, useEffect, and Custom Hooks",
    thumbnail: "/react-hooks-thumbnail.png",
    duration: "18:45",
    views: "856K",
    likes: "32K",
    publishedDate: "1 week ago",
    channel: {
      name: "CodeMaster",
      avatar: "/coding-channel-avatar.png",
      verified: false,
    },
    videoUrl: "/sample-video-2.mp4",
  },
  {
    id: 3,
    title: "CSS Grid vs Flexbox: When to Use Each Layout Method",
    thumbnail: "/css-layout-tutorial.png",
    duration: "15:22",
    views: "634K",
    likes: "28K",
    publishedDate: "3 days ago",
    channel: {
      name: "DesignDev",
      avatar: "/channel-avatar.png",
      verified: true,
    },
    videoUrl: "/sample-video-3.mp4",
  },
  {
    id: 4,
    title: "JavaScript ES2024 Features You Need to Know",
    thumbnail: "/javascript-features-thumbnail.png",
    duration: "22:18",
    views: "2.1M",
    likes: "87K",
    publishedDate: "5 days ago",
    channel: {
      name: "JS Weekly",
      avatar: "/javascript-channel-avatar.png",
      verified: true,
    },
    videoUrl: "/sample-video-4.mp4",
  },
  {
    id: 5,
    title: "Building a Full-Stack App with TypeScript and Prisma",
    thumbnail: "/fullstack-typescript-tutorial-thumbnail.png",
    duration: "45:12",
    views: "445K",
    likes: "19K",
    publishedDate: "1 day ago",
    channel: {
      name: "FullStack Pro",
      avatar: "/fullstack-channel-avatar.png",
      verified: false,
    },
    videoUrl: "/sample-video-5.mp4",
  },
  {
    id: 6,
    title: "Database Design Best Practices for Scalable Applications",
    thumbnail: "/database-design-tutorial.png",
    duration: "28:56",
    views: "723K",
    likes: "41K",
    publishedDate: "4 days ago",
    channel: {
      name: "DataBase Guru",
      avatar: "/database-channel-avatar.png",
      verified: true,
    },
    videoUrl: "/sample-video-6.mp4",
  },
]

// Utility functions
function formatNumber(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + "M"
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + "K"
  }
  return num.toString()
}

function createVideoCard(video) {
  return `
        <div class="video-card" data-video-id="${video.id}">
            <a href="/video/${video.id}" class="thumbnail-link">
                <div class="thumbnail-container">
                    <img src="${video.thumbnail || "/video-thumbnail.png"}" 
                         alt="${video.title}" 
                         loading="lazy">
                    <div class="duration-badge">${video.duration}</div>
                    <div class="hover-overlay"></div>
                </div>
            </a>
            
            <div class="video-info">
                <a href="/channel/${video.channel.name}" class="channel-avatar">
                    <img src="${video.channel.avatar || "/abstract-channel-avatar.png"}" 
                         alt="${video.channel.name}" 
                         loading="lazy">
                </a>
                
                <div class="video-details">
                    <div class="video-header">
                        <div class="video-content">
                            <a href="/video/${video.id}" class="video-title">
                                ${video.title}
                            </a>
                            
                            <a href="/channel/${video.channel.name}" class="channel-info">
                                <span class="channel-name">${video.channel.name}</span>
                                ${video.channel.verified ? '<i class="fas fa-check-circle verified-icon"></i>' : ""}
                            </a>
                            
                            <div class="video-stats">
                                <div class="stat-item">
                                    <i class="fas fa-eye stat-icon"></i>
                                    <span>${video.views} views</span>
                                </div>
                                <div class="stat-item">
                                    <i class="fas fa-thumbs-up stat-icon"></i>
                                    <span>${video.likes}</span>
                                </div>
                                <span class="stat-separator">•</span>
                                <span>${video.publishedDate}</span>
                            </div>
                        </div>
                        
                        <button class="more-options" data-video-id="${video.id}">
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `
}

// Dropdown menu functionality
let currentDropdown = null

function showDropdown(button, videoId) {
  hideDropdown()

  const dropdown = document.getElementById("dropdownMenu")
  const rect = button.getBoundingClientRect()

  dropdown.style.top = `${rect.bottom + window.scrollY + 5}px`
  dropdown.style.left = `${rect.left + window.scrollX - 150}px`
  dropdown.classList.add("show")
  dropdown.dataset.videoId = videoId

  currentDropdown = dropdown
}

function hideDropdown() {
  if (currentDropdown) {
    currentDropdown.classList.remove("show")
    currentDropdown = null
  }
}

function handleDropdownAction(action, videoId) {
  console.log(`Action: ${action} for video ${videoId}`)

  switch (action) {
    case "watch-later":
      alert(`Added video ${videoId} to Watch Later`)
      break
    case "playlist":
      alert(`Add video ${videoId} to Playlist`)
      break
    case "share":
      if (navigator.share) {
        navigator.share({
          title: "Check out this video",
          url: `/video/${videoId}`,
        })
      } else {
        alert(`Share video ${videoId}`)
      }
      break
    case "not-interested":
      alert(`Marked video ${videoId} as not interested`)
      break
    case "dont-recommend":
      alert(`Won't recommend this channel anymore`)
      break
    case "report":
      alert(`Report video ${videoId}`)
      break
  }

  hideDropdown()
}

// Initialize the application
function init() {
  const videoGrid = document.getElementById("videoGrid")

  // Render video cards
  mockVideos.forEach((video) => {
    videoGrid.innerHTML += createVideoCard(video)
  })

  // Add event listeners
  document.addEventListener("click", (e) => {
    // Handle more options button
    if (e.target.closest(".more-options")) {
      e.preventDefault()
      e.stopPropagation()
      const button = e.target.closest(".more-options")
      const videoId = button.dataset.videoId
      showDropdown(button, videoId)
      return
    }

    // Handle dropdown item clicks
    if (e.target.closest(".dropdown-item")) {
      e.preventDefault()
      const item = e.target.closest(".dropdown-item")
      const action = item.dataset.action
      const videoId = currentDropdown?.dataset.videoId
      if (action && videoId) {
        handleDropdownAction(action, videoId)
      }
      return
    }

    // Hide dropdown when clicking outside
    if (currentDropdown && !e.target.closest(".dropdown-menu")) {
      hideDropdown()
    }
  })

  // Handle escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && currentDropdown) {
      hideDropdown()
    }
  })

  // Handle video card hover effects
  document.querySelectorAll(".video-card").forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.classList.add("hovered")
    })

    card.addEventListener("mouseleave", () => {
      card.classList.remove("hovered")
    })
  })
}

// Start the application when DOM is loaded
document.addEventListener("DOMContentLoaded", init)

// Handle window resize for responsive dropdown positioning
window.addEventListener("resize", () => {
  if (currentDropdown) {
    hideDropdown()
  }
})
