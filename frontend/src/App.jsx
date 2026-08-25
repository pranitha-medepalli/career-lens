import {
  useState
} from "react";

import {
  HashRouter,
  Routes,
  Route,
  NavLink
} from "react-router-dom";

import FileUpload from "./components/FileUpload";

import Dashboard
  from "./pages/Dashboard";

import ResumeAnalysis
  from "./pages/ResumeAnalysis";

import CareerRoles
  from "./pages/CareerRoles";

import JobMatch
  from "./pages/JobMatch";

import {
  analyzeResumeRoles
} from "./services/api";


function App() {

  const [analysis, setAnalysis] =
    useState(null);

  const [resumeFile, setResumeFile] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const handleAnalyze = async (
    file
  ) => {

    setResumeFile(file);

    setLoading(true);

    setError("");

    try {

      const result =
        await analyzeResumeRoles(
          file
        );

      setAnalysis(result);

    } catch (err) {

      console.error(err);

      setError(
        err?.response?.data?.detail ||
        "Unable to analyze the resume."
      );

    } finally {

      setLoading(false);

    }
  };


  const handleNewResume = () => {

    setAnalysis(null);

    setResumeFile(null);

    setError("");

  };


  return (

    <HashRouter>

      <div className="app">


        {/* ==========================
            NAVBAR
        =========================== */}

        <header className="navbar">

          <div className="brand">

            <div className="brand-icon">
              CL
            </div>

            <div>

              <h1>
                Career Lens
              </h1>

              <span>
                See how your resume fits the job.
              </span>

            </div>

          </div>


          {analysis && (

            <nav className="nav-links">

              <NavLink to="/">
                Dashboard
              </NavLink>

              <NavLink to="/resume">
                Resume
              </NavLink>

              <NavLink to="/roles">
                Career Roles
              </NavLink>

              <NavLink to="/job-match">
                Job Match
              </NavLink>

            </nav>

          )}

        </header>


        <main className="main-content">


          {/* =================================
              NO RESUME
          ================================= */}

          {!analysis && (

            <section className="hero">

              <div className="hero-copy">

                <span className="eyebrow">
                  CAREER LENS
                </span>

                <h2>
                  Understand where your
                  <span> resume </span>
                  can take you.
                </h2>

                <p>
                  Upload your resume and get
                  personalized career roles,
                  skill insights, and practical
                  next steps.
                </p>

              </div>


              <FileUpload
                onAnalyze={
                  handleAnalyze
                }
                loading={loading}
              />


              {error && (

                <div className="error-box">
                  {error}
                </div>

              )}

            </section>

          )}


          {/* =================================
              APPLICATION
          ================================= */}

          {analysis && (

            <Routes>

              <Route
                path="/"
                element={
                  <Dashboard
                    analysis={analysis}
                  />
                }
              />

              <Route
                path="/resume"
                element={
                  <ResumeAnalysis
                    analysis={analysis}
                  />
                }
              />

              <Route
                path="/roles"
                element={
                  <CareerRoles
                    analysis={analysis}
                  />
                }
              />

              <Route
                path="/job-match"
                element={
                  resumeFile ? (
                    <JobMatch
                      resumeFile={
                        resumeFile
                      }
                    />
                  ) : null
                }
              />

            </Routes>

          )}

        </main>

      </div>

    </HashRouter>

  );
}


export default App;