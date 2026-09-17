import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Login from "./pages/Login";
import Halls from "./pages/Halls";
import OwnerDashboard from "./pages/OwnerDashboard";

function Header() {
    const navigate = useNavigate();

    function handleLogout() {
        localStorage.removeItem("token");
        navigate("/login");
    }

    if (window.location.pathname === "/login") {
        return null;
    }

    return (
        <header className="app-header">
            <button onClick={handleLogout} id="sss">
                Logout
            </button>
        </header>
    );
}

function App() {
    return (
        <BrowserRouter>
            <Header />

            <Routes>
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="/login" element={<Login />} />
                <Route path="/halls" element={<Halls />} />
                <Route path="/owner" element={<OwnerDashboard />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;