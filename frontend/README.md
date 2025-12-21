# ATS Resume Analyzer - Frontend

Modern Next.js frontend for the AI-Powered Resume ATS Analyzer.

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend server running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at [http://localhost:3000](http://localhost:3000)

### Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📁 Project Structure

```
frontend/
├── components/          # React components
│   ├── FileUpload.jsx   # File upload with drag & drop
│   ├── ScoreGauge.jsx   # Circular score visualization
│   ├── KeywordList.jsx  # Keyword display component
│   └── ReportCard.jsx  # Report display component
├── pages/              # Next.js pages
│   ├── _app.js         # App wrapper
│   ├── index.js        # Upload page
│   └── report/[id].js  # Report display page
├── lib/                # Utilities
│   └── api.js          # API client
├── styles/             # Styles
│   └── globals.css     # Global styles & Tailwind
└── public/             # Static assets
```

## 🎨 Features

- ✅ Modern, clean UI design
- ✅ Drag & drop file upload
- ✅ Real-time score visualization
- ✅ Responsive design
- ✅ Loading states and error handling
- ✅ Smooth animations
- ✅ TailwindCSS styling

## 🛠️ Build

```bash
# Production build
npm run build

# Start production server
npm start
```

## 📝 License

See main project LICENSE file.


