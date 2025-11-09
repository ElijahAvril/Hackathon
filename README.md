#  Multilingual Conversation Partner

> **Break the language barrier — one voice at a time.**

A Flask-based web application that enables real-time, AI-powered multilingual conversations.  
Built using **Google Gemini** for text generation, **Whisper** for speech-to-text, and **ElevenLabs** for realistic text-to-speech audio output.

---

##  Inspiration
We wanted to make communication more natural and inclusive — no matter the language you speak.  
*Multilingual Conversation Partner* bridges that gap, letting users talk, listen, and learn across languages with the help of AI.

---

##  What It Does
-  Converts your speech to text using **Whisper**  
-  Generates AI responses through **Gemini** in your selected language  
-  Speaks the reply naturally via **ElevenLabs**  
-  Displays the conversation seamlessly through a simple web interface

Whether you’re practicing a language or holding a real-time multilingual chat, it feels intuitive, fluid, and human.

---

##  Architecture Overview


**Workflow Summary:**
1. User speaks or types a message in their selected language.  
2. Whisper transcribes the audio to text.  
3. Gemini generates a context-aware, multilingual AI response.  
4. ElevenLabs converts that text into natural speech.  
5. The spoken response plays directly on the web interface.

---

## Tech Stack

| Layer | Technology |
|--------|-------------|
| Backend | Python (Flask) |
| AI Model | Google Gemini API |
| Speech-to-Text | Whisper |
| Text-to-Speech | ElevenLabs API |
| Frontend | HTML, CSS, JavaScript |
| Environment Management | python-dotenv |

---

## Usage

1. Choose your desired language from the dropdown menu.

2. Record or type your message.

3. Let the AI reply — and listen to it speak back naturally!

This creates an immersive experience for multilingual learners, travelers, and conversational AI enthusiasts.

## Team & Contributions

Elijah - AI Integration:	Connected Gemini and ElevenLabs APIs, optimized response generation, and ensured language fidelity.

Nathan	- Frontend & Backend:	Built Flask routing, request handling, and created the language-select UI with responsive design.

Julia	- Creative Director:	Designed UI layout, presentation visuals, and oversaw user experience and project branding.

Together, we combined engineering, AI, and creativity to make seamless communication possible.
