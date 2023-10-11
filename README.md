# Vinted Curation Bot - A Rebel in the Fashion World 🚀

## Overview

Welcome to the Vinted Curation Bot, where technology meets sustainable fashion, and where we say a big "No Thanks" to the fast-fashion industry. This bot is not just a piece of code; it's a statement, a stand against the ecological and ethical nightmares of the fashion industry. It’s a blend of tech and eco-consciousness, automating the curation of second-hand fashion items from Vinted, and serving them up to style-hungry, yet eco-aware folks.

## Why?

- **Sustainable Fashion:** We're tired of the fast-fashion industry and its impact on our planet. Second-hand shopping is not just a trend; it's a statement, a lifestyle, and a little revolution.
  
- **Tech for Good:** We utilize technology to promote sustainable habits, making second-hand shopping a breeze, and curating fashion that doesn’t cost the earth (literally).

## How it Works

### 1. Data Retrieval 🕵️‍♂️

- **API Requests:** The bot sends tailored requests to Vinted’s API, hunting down items based on predefined criteria like brand, color, and keywords.
  
- **Data Handling:** It processes the retrieved data, filtering items based on algorithms that consider historical retention rates per brand.

### 2. Manual Validation 🧐

- **Backend UI:** Utilizing Streamlit, a backend UI presents the pre-selected items for manual validation, ensuring only the coolest pieces make the cut.

### 3. Synchronization with Raindrop.io 🔄

- **API Integration:** Upon validation, the bot communicates with Raindrop.io’s API, updating the platform with the latest approved items.

### 4. Availability Check 🛒

- **Daily Checks:** The bot performs daily checks on Vinted to ensure each item is still available, maintaining a fresh and accurate catalog.

### 5. Stock Management 📦

- **Quota System:** It manages stock, ensuring a balanced and varied selection, adhering to predefined quotas for each size and category.

## Tech Stack

- **Python:** For data retrieval, processing, and bot logic.
  
- **Streamlit:** For backend UI and manual validation.
  
- **Raindrop.io API:** For data synchronization and sharing curated items.

## Future Enhancements 🔮

- **Docker:** Ensuring smooth deployment and scalability.
  
- **Symfony:** For a robust and flexible backend.
  
- **Next.js & TailwindCSS:** Crafting a modern, responsive frontend.

## Code Notice ⚠️

Please note that the code for this project isn't super clean and is quite procedural. It was my first project ever, and while it might not be a paragon of best practices, it's a testament to my journey and learning curve in the world of development.

## Join the Rebellion 🚀

This bot is more than a project; it’s a rebellion against fast fashion, a stand for our planet, and a nod to the power of tech. It’s a journey from sustainability to style, all while keeping it digital and ethical. So, if you’re tired of the fashion industry’s antics and believe in the power of second-hand, join us. Let’s code, curate, and save the planet, one stylish outfit at a time.
