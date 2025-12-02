# iLearning AI Education Full Stack Project

This project is an AI-powered learning platform focused on generating and grading essays/MCQs and offering tutoring-style chats on uploaded educational content. 
- The backend is built with Python and FastAPI, fronted by NGINX as an API gateway, and integrates Google Gemini (via the `google-genai` client) with Pydantic for configuration and data models. 
    - Future features (enable them later)
        - Rate limiting, caching, TLS termination, auth, etc
- Frontend development is temporarily on hold while the backend API and infrastructure are being stabilized.
    - Programming: TypeScript
    - Framework / Routing: SvelteKit
    - State Management: Svelte stores (writable / derived)
    - UI Library / Styling: TailwindCSS
- Database: MongoDB (NoSQL DB)
- Deployment: Terraform +  GKE
