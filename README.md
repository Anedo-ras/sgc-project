AI Productivity Suite

AI Productivity Suite is a full-stack web app designed to help users boost productivity through mood journaling, AI study flashcards, and recipe recommendations. It combines Flask + Supabase/MySQL + modern HTML/CSS/JS frontend, with AI APIs and IntaSend payment integration for monetization.

📌 Features
1. 📝 Mood Journal

Users can enter a daily journal entry.

Flask sends entry → Hugging Face Sentiment API.

Sentiment score + text stored in Supabase/MySQL DB.

Visualize mood trends with Chart.js.

2. 📚 AI Study Buddy

Users paste study notes into a form.

Flask sends notes → Hugging Face Q&A API → generates 5 flashcards.

Flashcards stored in DB.

Displayed as interactive flip-cards (HTML/CSS/JS).

3. 🍳 Recipe Recommender

Users select ingredients from a multi-input form.

Flask sends query → OpenAI API → returns 3 recipe suggestions.

Recipes stored in DB under the user profile.

Displayed as clickable recipe cards.

4. 💳 Monetization (IntaSend Integration)

Users can upgrade to premium for:

Unlimited flashcards

Detailed mood reports

Personalized meal plans

Payment powered by IntaSend (via embedded JS SDK).

Supports one-time purchases (e.g., PDF export).

🛠️ Tech Stack
Frontend

HTML5, CSS3 (minimal, modern design)

Vanilla JavaScript (interactivity)

Chart.js (data visualization)

Backend

Python + Flask (API routes & business logic)

Database

Supabase (Postgres, real-time) or MySQL (local testing)

APIs

Hugging Face API – sentiment analysis & Q&A generation

OpenAI API – recipe suggestions

IntaSend API – payments

Deployment

Built for Bolt.new fast deployment
