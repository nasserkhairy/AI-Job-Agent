import { useState, useEffect } from "react";
import axios from "axios";
import toast from "react-hot-toast";

function App() {
  const [file, setFile] = useState(null);
  const [jobUrl, setJobUrl] = useState("");
  const [result, setResult] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/profile"
      );

      if (!response.data.error) {
        setProfile(response.data);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const uploadCV = async () => {
    if (!file) {
      toast.error("Please select a CV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(
        "http://127.0.0.1:8000/upload-cv",
        formData
      );

      toast.success("CV uploaded successfully");

      loadProfile();
    } catch (error) {
      console.error(error);
      toast.error("Failed to upload CV");
    }
  };

  const analyzeJob = async () => {
    if (!jobUrl) {
      toast.error("Please enter a job URL");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze-job-url",
        {
          url: jobUrl,
        }
      );

      if (response.data.error) {
        toast.error(response.data.error);
        return;
      }

      setResult(response.data);

      toast.success("Analysis completed");
    } catch (error) {
      console.error(error);
      toast.error("Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const markApplied = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/mark-applied",
        {
          url: jobUrl,
        }
      );

      setResult({
        ...result,
        already_applied: true,
      });

      toast.success("Job marked as applied");
    } catch (error) {
      console.error(error);
      toast.error("Operation failed");
    }
  };

  const scoreColor =
    result?.match_score >= 80
      ? "bg-success"
      : result?.match_score >= 60
      ? "bg-warning"
      : "bg-danger";

  return (
    <div className="container py-5">

      <div className="text-center mb-5">
        <h1 className="fw-bold">AI Job Agent</h1>

        <p className="text-muted">
          Match your CV against jobs and generate cover letters
        </p>
      </div>

      {profile && (
        <div className="card shadow-sm mb-4 border-0">
          <div className="card-body">

            <h3 className="fw-bold">
              {profile.name}
            </h3>

            <p className="text-muted mb-2">
              {profile.title}
            </p>

            <p>
              <strong>Experience:</strong>{" "}
              {profile.years_experience} years
            </p>

            <h6 className="mt-3">
              Skills
            </h6>

            <div>
              {profile.skills?.map((skill, index) => (
                <span
                  key={index}
                  className="badge bg-primary me-2 mb-2"
                >
                  {skill}
                </span>
              ))}
            </div>

          </div>
        </div>
      )}

      <div className="card shadow-sm mb-4 border-0">
        <div className="card-body">

          <h4 className="mb-3">
            Upload CV
          </h4>

          <div className="row g-2">

            <div className="col-md-9">
              <input
                type="file"
                className="form-control"
                accept=".pdf"
                onChange={(e) =>
                  setFile(e.target.files[0])
                }
              />
            </div>

            <div className="col-md-3">
              <button
                className="btn btn-success w-100"
                onClick={uploadCV}
              >
                Upload CV
              </button>
            </div>

          </div>

        </div>
      </div>

      <div className="card shadow-sm mb-4 border-0">
        <div className="card-body">

          <h4 className="mb-3">
            Analyze Job
          </h4>

          <input
            type="text"
            className="form-control mb-3"
            placeholder="Paste job URL here..."
            value={jobUrl}
            onChange={(e) =>
              setJobUrl(e.target.value)
            }
          />

          <button
            className="btn btn-primary"
            onClick={analyzeJob}
            disabled={loading}
          >
            {loading ? (
              <>
                <span
                  className="spinner-border spinner-border-sm me-2"
                ></span>
                Analyzing...
              </>
            ) : (
              "Analyze Job"
            )}
          </button>

        </div>
      </div>

      {result && (
        <div className="card shadow border-0">
          <div className="card-body">

            <div className="d-flex justify-content-between align-items-center mb-3">

              <h3 className="mb-0">
                Match Score
              </h3>

              {result.already_applied ? (
                <span className="badge bg-warning text-dark fs-6">
                  Already Applied
                </span>
              ) : (
                <span className="badge bg-success fs-6">
                  Not Applied Yet
                </span>
              )}

            </div>

            <h2 className="fw-bold">
              {result.match_score}%
            </h2>

            <div className="progress mb-4">
              <div
                className={`progress-bar ${scoreColor}`}
                role="progressbar"
                style={{
                  width: `${result.match_score}%`,
                }}
              >
                {result.match_score}%
              </div>
            </div>

            {!result.already_applied && (
              <button
                className="btn btn-warning mb-4"
                onClick={markApplied}
              >
                Mark As Applied
              </button>
            )}

            <h4>Strengths</h4>

            <ul className="list-group mb-4">
              {result.strengths?.map(
                (item, index) => (
                  <li
                    key={index}
                    className="list-group-item"
                  >
                    {item}
                  </li>
                )
              )}
            </ul>

            <h4>Missing Skills</h4>

            <ul className="list-group mb-4">
              {result.missing_skills?.map(
                (item, index) => (
                  <li
                    key={index}
                    className="list-group-item"
                  >
                    {item}
                  </li>
                )
              )}
            </ul>

            <h4>Recommendation</h4>

            <div className="alert alert-info">
              {result.recommendation}
            </div>

            <h4>Cover Letter</h4>

            <textarea
              className="form-control"
              rows="12"
              value={result.cover_letter}
              readOnly
            />

          </div>
        </div>
      )}

    </div>
  );
}

export default App;