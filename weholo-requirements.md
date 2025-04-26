# WeHolo

WeHolo is an online platform that provides users with a fun and interactive experience using 3D avatars powered by AI. Users can pick avatars, talk to them using text or voice, and see the avatars respond with animations like lip-syncing, gestures, and emotions. The platform works on any device connected to a holographic display. Below are the features and what needs to be built:

## Key Features for Users

### 1. User Accounts (Authentication System)
- **Sign Up**: Users can create an account using email and password.
- **Log In**: Users with an account can log in to access their personalized settings.

### 2. Dashboard
- **Persona Setup**: Users can:
  - Create Custom Avatars
  - Adjust avatar behavior
  - Change camera modes
  - Pick their language
  - Customize the user interface
- **Interaction Interface**: Users can chat with their avatars using text or video.

### 3. Gallery (Akool API)
- Displays a list of avatars that users can choose from.
- Avatars may include pre-designed options with unique behaviors and styles.

### 4. Studio
- Offers tools to:
  - Design and customize avatars (appearance, behavior, etc.)
  - Personalize avatars according to user preferences

### 5. Demo Section
- A place where users can see pre-recorded demonstrations of avatars in action.

### 6. Interactive Chat
- **Real-Time Messaging**: Users can send messages and get responses from avatars.
- **Video Interaction**: Allows for a more engaging experience with video elements.

### 7. Responsive Design
- The platform should work smoothly on different devices (desktop, tablet, mobile).

## Using AKOOL and Soul Machines APIs

### AKOOL Features (For Low-Budget Users)
- **Avatar Selection**: Users can choose from 130+ pre-made avatars.
- **Voice Options**: 500+ voices available, or clone a custom voice.
- **Multilingual Support**: Create content in 150+ languages with accurate lip-sync and movements.
- **Video Quality**: Videos can be exported in up to 4K resolution.
- **Custom Avatars**: Users can upload photos to create unique avatars.

### Soul Machines Features (For High-Budget Users)
- **Custom Avatars**: Fully customizable avatars with specific looks, tones, and personalities.
- **AI Assistant Deployment**: Set up and launch avatars as digital assistants.
- **Object Recognition and Memory**: Avatars can recognize objects and remember users for personalized interactions.
- **Human-Like Interaction**: Avatars can see, hear, and express emotions naturally.

## Additional Features to Build

### 1. Subscription System
- Users on a low budget can choose AKOOL's basic features (e.g., video recording with avatars).
- Users on a high budget can opt for Soul Machines' interactive features (e.g., live interaction with avatars).

### 2. Product Display
- When an avatar talks about a product, it should display an image of the product from the database.
- The database will store products that users have saved or added.

### 3. Beginner-Friendly Bot
- For users who are not tech-savvy:
  - They can chat with a bot to describe the kind of avatar they want.
  - The bot will recommend an avatar from AKOOL's pre-designed options.

### 4. Cached Conversations
- Conversations should be stored locally or temporarily synced to minimize frequent API calls. This will improve speed and reduce costs.

## Developer's Focus Points

### 1. APIs to Implement:
- AKOOL API for avatar creation and videos.
- Soul Machines API for interactive, human-like experiences.

### 2. Database Requirements:
- User profiles, preferences, and saved data.
- Product images and details for avatar mentions.

### 3. Caching System:
- Store recent conversations locally to reduce API usage.

### 4. Subscription Management:
- Create a payment system to separate low-budget and high-budget features.

### 5. User-Friendly Bot:
- Develop an intuitive chatbot to guide users in selecting avatars.
