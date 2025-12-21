import '../styles/globals.css';
import Head from 'next/head';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>ATS Resume Analyzer - AI-Powered Resume Analysis</title>
        <meta
          name="description"
          content="Analyze your resume against job descriptions using AI-powered ATS scoring"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;


