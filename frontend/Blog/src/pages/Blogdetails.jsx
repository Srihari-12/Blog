// BlogDetails.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import {
  Box,
  Typography,
  Container,
  TextField,
  Button,
  Divider,
  Paper,
} from "@mui/material";

const API_URL = "http://127.0.0.1:8000/api/v1";

const BlogDetails = () => {
  const { id } = useParams();
  const token = localStorage.getItem("token");
  const [blog, setBlog] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState("");

  const fetchBlogDetails = async () => {
    const res = await axios.get(`${API_URL}/blogs/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setBlog(res.data);
  };

  const fetchComments = async () => {
    const res = await axios.get(`${API_URL}/blogs/${id}/comments`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setComments(res.data);
  };

  const postComment = async () => {
    await axios.post(
      `${API_URL}/blogs/${id}/comments`,
      { content: commentText },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setCommentText("");
    fetchComments();
  };

  useEffect(() => {
    if (token) {
      fetchBlogDetails();
      fetchComments();
    }
  }, [id]);

  if (!blog) return <Typography>Loading...</Typography>;

  return (
    <Container sx={{ mt: 6 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          {blog.title}
        </Typography>
        <Typography variant="subtitle2" gutterBottom>
          By {blog.author_email}
        </Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          {blog.content}
        </Typography>
      </Paper>

      <Box mt={5}>
        <Typography variant="h5">Comments</Typography>
        {comments.map((c, idx) => (
          <Paper key={idx} sx={{ p: 2, mt: 2 }}>
            <Typography variant="body2">{c.content}</Typography>
            <Typography variant="caption">- {c.author_email}</Typography>
          </Paper>
        ))}

        <Box mt={3}>
          <TextField
            label="Write a comment"
            fullWidth
            multiline
            rows={3}
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button variant="contained" onClick={postComment}>
            Post Comment
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default BlogDetails;