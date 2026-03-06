# 🎨 ATS Resume Analyzer - Frontend

<div align="center">

[![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

**Modern React Frontend | Server-Side Rendering | Responsive Design**

[Quick Start](#-quick-start) • [Features](#-features) • [Components](#-components) • [Deployment](#-deployment)

</div>

---

## 📋 Overview

Modern, responsive **Next.js** frontend providing an intuitive user interface for the ATS Resume Analyzer. Features include drag-and-drop file uploads, real-time score visualization, smooth animations, and comprehensive error handling.

**Key Features:**
- ✅ **Next.js 14** - React framework with SSR and optimized performance
- ✅ **TailwindCSS** - Utility-first CSS for rapid UI development
- ✅ **Responsive Design** - Mobile, tablet, and desktop optimized
- ✅ **Real-time Feedback** - Loading states, progress indicators, error handling
- ✅ **Smooth Animations** - Framer Motion for polished UX
- ✅ **Accessibility** - WCAG-compliant components

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Application                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Pages Layer (pages/)                            │  │
│  │  • index.js - Upload page                        │  │
│  │  • report/[id].js - Dynamic report page          │  │
│  │  • _app.js - App wrapper & global styles         │  │
│  └───────────────┬───────────────────────────────────┘  │
│                  │                                       │
│  ┌───────────────▼───────────────────────────────────┐  │
│  │  Components Layer (components/)                    │  │
│  │  ┌─────────────────────────────────────────────┐ │  │
│  │  │ FileUpload.jsx - Drag & drop upload         │ │  │
│  │  │ ScoreGauge.jsx - Circular score display     │ │  │
│  │  │ ReportCard.jsx - Report visualization       │ │  │
│  │  │ KeywordList.jsx - Keyword display           │ │  │
│  │  │ ErrorMessage.jsx - Error handling           │ │  │
│  │  │ LoadingSpinner.jsx - Loading states         │ │  │
│  │  └─────────────────────────────────────────────┘ │  │
│  └───────────────┬───────────────────────────────────┘  │
│                  │                                       │
│  ┌───────────────▼───────────────────────────────────┐  │
│  │  API Layer (lib/api.js)                           │  │
│  │  • Axios client with interceptors                 │  │
│  │  • Error handling                                 │  │
│  │  • Request/response transformation                │  │
│  └───────────────┬───────────────────────────────────┘  │
└──────────────────┼───────────────────────────────────────┘
                   │ HTTPS/REST API
                   ▼
            ┌──────────────┐
            │  FastAPI     │
            │   Backend    │
            └──────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Next.js | 14+ | React framework with SSR |
| **UI Library** | React | 18+ | Component-based UI |
| **Styling** | TailwindCSS | 3.3+ | Utility-first CSS |
| **HTTP Client** | Axios | 1.6+ | API communication |
| **Animations** | Framer Motion | 12+ | Smooth animations |
| **Icons** | Lucide React | 0.294+ | Modern icon library |
| **File Upload** | react-dropzone | 14+ | Drag & drop file upload |

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18.x or 20.x
- **npm** or **yarn** package manager
- **Backend API** running (see [backend README](../backend/README.md))

### Installation

```bash
# Clone repository
git clone https://github.com/ashwin-portfolio/ats-resume-analyzer.git
cd ats-resume-analyzer/frontend

# Install dependencies
npm install
# or
yarn install
```

### Environment Configuration

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note:** The `NEXT_PUBLIC_` prefix is required for client-side access in Next.js.

### Development Server

```bash
# Start development server
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

---

## ✨ Features

### 🎯 User Experience
- **Drag & Drop Upload** - Intuitive file upload interface
- **Real-time Validation** - Instant feedback on file selection
- **Progress Indicators** - Visual feedback during analysis
- **Error Handling** - User-friendly error messages
- **Success Notifications** - Clear confirmation messages

### 📊 Data Visualization
- **Circular Score Gauge** - Animated ATS score display
- **Keyword Lists** - Matched and missing keywords
- **Report Cards** - Comprehensive report visualization
- **Responsive Charts** - Mobile-optimized visualizations

### 🎨 Design
- **Modern UI** - Clean, professional design
- **Gradient Backgrounds** - Eye-catching visual elements
- **Smooth Animations** - Framer Motion transitions
- **Responsive Layout** - Works on all screen sizes
- **Dark Mode Ready** - Theme support (future enhancement)

---

## 📁 Project Structure

```
frontend/
├── components/              # Reusable React components
│   ├── FileUpload.jsx      # Drag & drop file upload component
│   ├── ScoreGauge.jsx      # Circular score visualization
│   ├── ReportCard.jsx     # Report display component
│   ├── KeywordList.jsx    # Keyword display component
│   ├── ErrorMessage.jsx   # Error message component
│   ├── LoadingSpinner.jsx # Loading indicator
│   └── SuccessMessage.jsx # Success notification
│
├── pages/                  # Next.js pages (routing)
│   ├── _app.js            # App wrapper & global configuration
│   ├── index.js           # Upload page (home)
│   └── report/
│       └── [id].js        # Dynamic report page
│
├── lib/                    # Utilities and helpers
│   └── api.js             # API client with Axios
│
├── styles/                 # Global styles
│   └── globals.css        # Global CSS & Tailwind imports
│
├── public/                 # Static assets
│   └── favicon.ico        # Site favicon
│
├── next.config.js          # Next.js configuration
├── tailwind.config.js      # TailwindCSS configuration
├── postcss.config.js       # PostCSS configuration
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

---

## 🧩 Components

### FileUpload
Drag-and-drop file upload with validation.

**Features:**
- Drag & drop support
- File type validation (PDF, DOCX)
- File size validation (10MB max)
- Visual feedback
- Error handling

### ScoreGauge
Animated circular gauge for ATS score display.

**Features:**
- Smooth animations
- Color-coded scores (red/yellow/green)
- Percentage display
- Responsive sizing

### ReportCard
Comprehensive report visualization component.

**Features:**
- ATS score display
- Skill match percentage
- Keyword lists (matched/missing)
- Recommendations
- Summary text

### KeywordList
Display list of keywords with relevance scores.

**Features:**
- Categorized display (matched/missing)
- Relevance indicators
- Color coding
- Responsive grid layout

---

## 🎨 Styling

### TailwindCSS Configuration

Custom theme configuration in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#...',
      secondary: '#...',
    },
  },
}
```

### Global Styles

Global styles and Tailwind imports in `styles/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
```

---

## 🔌 API Integration

### API Client

The API client (`lib/api.js`) provides:

- **Axios instance** with base configuration
- **Request interceptors** for error handling
- **Response interceptors** for data transformation
- **Timeout handling** (60s default, 120s for analysis)
- **Error formatting** - User-friendly error messages

### Usage Example

```javascript
import api from '../lib/api';

// Upload and analyze resume
const formData = new FormData();
formData.append('resume_file', file);
formData.append('job_description', jobDescription);

const response = await api.post('/api/v1/analyze', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
  timeout: 120000, // 2 minutes for analysis
});
```

---

## 🚢 Deployment

### Vercel (Recommended)

1. **Connect Repository**
   - Go to [Vercel](https://vercel.com)
   - Import GitHub repository
   - Select `frontend` as root directory

2. **Configure Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```

3. **Deploy**
   - Vercel auto-detects Next.js
   - Builds and deploys automatically
   - Provides production URL

### Other Platforms

**Netlify:**
```bash
npm run build
# Deploy .next folder
```

**AWS Amplify:**
- Connect repository
- Set build command: `npm run build`
- Set output directory: `.next`

### Environment Variables

For production, set:
```env
NEXT_PUBLIC_API_URL=https://your-production-api.com
```

---

## 🧪 Testing

```bash
# Run linter
npm run lint

# Type checking (if TypeScript)
npm run type-check

# Build test
npm run build
```

---

## 📊 Performance Optimization

### Next.js Optimizations

- ✅ **Server-Side Rendering** - Faster initial page load
- ✅ **Code Splitting** - Automatic route-based splitting
- ✅ **Image Optimization** - Next.js Image component
- ✅ **Static Generation** - Pre-rendered pages where possible

### Best Practices

- ✅ **Component Lazy Loading** - Load components on demand
- ✅ **Memoization** - React.memo for expensive components
- ✅ **Debouncing** - Input debouncing for search/validation
- ✅ **Error Boundaries** - Graceful error handling

---

## 🎓 Technical Highlights

- ✅ **Server-Side Rendering** - SEO-friendly and fast initial load
- ✅ **Component Reusability** - Modular, reusable components
- ✅ **State Management** - React hooks for state management
- ✅ **Error Handling** - Comprehensive error boundaries
- ✅ **Responsive Design** - Mobile-first approach
- ✅ **Accessibility** - ARIA labels and keyboard navigation
- ✅ **Performance** - Optimized bundle size and loading

---

## 🔮 Future Enhancements

- [ ] **TypeScript Migration** - Full type safety
- [ ] **Dark Mode** - Theme switching
- [ ] **PWA Support** - Progressive Web App features
- [ ] **Offline Support** - Service worker implementation
- [ ] **Advanced Animations** - More interactive transitions
- [ ] **Internationalization** - Multi-language support
- [ ] **Analytics** - User behavior tracking
- [ ] **A/B Testing** - Feature experimentation

---

## 📖 Documentation

- **Main Project README**: [../README.md](../README.md)
- **Backend API**: [../backend/README.md](../backend/README.md)
- **Deployment Guide**: [../docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

<div align="center">

**Part of the [ATS Resume Analyzer](../README.md) project**

*Built with ❤️ using Next.js and modern React best practices*</div>
