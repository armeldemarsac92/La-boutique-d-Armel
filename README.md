# Vinted Curation Platform - Leading the Revolution in Sustainable Fashion 🚀

## Overview

Welcome to the Vinted Curation Platform, a sophisticated intersection of technology and sustainable fashion. This platform, powered by intelligent bots, serves as a pioneer in challenging the fast-fashion industry. It's not merely about automation; it's about creating a community where influencers and super users can curate a unique, eco-conscious shopping experience for their followers.

## Motivation

- **Sustainable Fashion**: Taking a stand against the harmful impacts of the fast-fashion industry, our platform champions second-hand shopping. This movement isn't just a fleeting trend but a commitment to a more eco-friendly and conscious lifestyle.
- **Harnessing Technology**: By leveraging cutting-edge tech, we've transformed the face of second-hand shopping, presenting curated, sustainable fashion choices with a touch of personalization.

## Architecture & Workflow

1. **Admin Dashboard (Next.js App)**:
    - A specialized interface for boutique administrators to define brands, colors, keywords, and more, all stored in a MySQL database.
    - Categories can be crafted, each housing specific "request" objects that guide the behavior of scrapping bots.
    - A Tinder-inspired interface is available for reviewing newly added items. Items that resonate are highlighted on the frontend, while others remain concealed.

2. **Backend (Symfony)**:
    - Functions as an API, addressing HTTP requests from both the admin dashboard and frontend.
    - Deploys "request" objects from the dashboard to initiate new tasks in a Rabbit MQ queue, signaling the scrapping bots.

3. **Scrapping Bots (Python Scripts in Docker)**:
    - These dockerized bots monitor the primary Rabbit MQ queue, fetching URLs derived from request parameters.
    - Secondary Python scripts extract data from these URLs, subsequently passing the information to a Symfony controller via another Rabbit MQ queue.

4. **Database Management**:
    - The Symfony controller commits item data to a MariaDB MySQL server.
    - Regular checks are conducted to refresh item availability. Items no longer available are updated accordingly.
    - Should the number of items in a category dip below a set threshold, a new data fetch is activated.

5. **User Experience**:
    - Users can earmark favorite items, streamlining their browsing experience.
    - Each brand is linked to its official URL, granting users the opportunity to delve deeper into brand narratives and ethos.

6. **Empowering Influencers**:
    - The platform is designed to accommodate multiple 'super user' accounts.
    - Influencers can mold their personalized curation interface, guiding their audience towards sustainable fashion choices.
    - Their ability to like or dislike items ensures a bespoke, curated experience for their community, reflecting the influencer's unique taste and style.

## Tech Stack

- **Python**: Drives data retrieval, powers scrapping bots, and oversees bot logic.
- **Symfony**: Manages backend operations and API functionalities.
- **Next.js**: Shapes the frontend and admin dashboard.
- **Docker**: Ensures scalability by containerizing all components, except for the MySQL database.
- **Rabbit MQ**: Orchestrates efficient data processing through message queuing.
- **MariaDB MySQL**: Handles robust database management.

## Future Roadmap

- **Personalized Recommendations**: By segmenting datasets and deploying new Python scripts.
- **Community Expansion**: Enabling influencers to architect their unique curation platforms, nurturing a dynamic, engaged community.

## Join the Movement 🚀

This platform represents more than just tech; it's a vibrant community rallying against fast fashion. Advocating sustainability and harnessing the prowess of technology, influencers and super users play a pivotal role in curating a tailored experience. If you share our passion and vision, join us. Let's reshape the fashion landscape, one curated choice at a time.
