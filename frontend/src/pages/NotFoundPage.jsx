import { Link } from "react-router-dom";

export default function NotFoundPage() {
    return (
        <div className="center-page">
            <div className="card auth-card">
                <h2>Page Not Found</h2>
                <p className="subtle">The page you requested does not exist.</p>
                <Link to="/dashboard" className="primary-link">
                    Go to Dashboard
                </Link>
            </div>
        </div>
    );
}