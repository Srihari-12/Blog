import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/landing";
import BlogPage from "./pages/Blogpage";
import BlogDetails from "./pages/Blogdetails";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route path="/blogs" element={<BlogPage />} />
        <Route path="/blogs/:id" element={<BlogDetails />} />
        <Route path="/blogs/:id/comments" element={<BlogDetails />} />
        <Route path="/blogs/:id/edit" element={<BlogDetails />} />
        
      </Routes>
    </Router>
  );
}

export default App;
