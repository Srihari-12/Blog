// landing.jsx
import { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  Card,
  CardContent,
  Grid,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { motion } from "framer-motion";

export default function LandingPage() {
  const [email, setEmail] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");
  const navigate = useNavigate();

  const handleSendOtp = async () => {
    await axios.post("http://localhost:8000/api/v1/send-otp", { email });
    setOtpSent(true);
  };

  const handleVerifyOtp = async () => {
    const res = await axios.post("http://localhost:8000/api/v1/verify-otp", {
      email,
      otp,
    });
    localStorage.setItem("access_token", res.data.access_token);
    navigate("/blogs");
  };

  return (
    <Box sx={{ minHeight: "100vh", background: "linear-gradient(120deg, #ccff00, #495d00)", p: 4 }}>
      <Container maxWidth="md">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <Typography variant="h3" fontWeight={700} mb={2} color="white">
            Blogify - Discover Thoughts
          </Typography>
          <Typography variant="h6" mb={4} color="white">
            Enter your email to get started with exploring blogs.
          </Typography>

          <Box>
            <TextField
              label="Email"
              variant="outlined"
              fullWidth
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              sx={{ mb: 2, backgroundColor: "white", borderRadius: 1 }}
            />

            {otpSent ? (
              <>
                <TextField
                  label="Enter OTP"
                  variant="outlined"
                  fullWidth
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  sx={{ mb: 2, backgroundColor: "white", borderRadius: 1 }}
                />
                <Button variant="contained" color="secondary" onClick={handleVerifyOtp}>
                  Verify OTP
                </Button>
              </>
            ) : (
              <Button variant="contained" color="primary" onClick={handleSendOtp}>
                Send OTP
              </Button>
            )}
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
}