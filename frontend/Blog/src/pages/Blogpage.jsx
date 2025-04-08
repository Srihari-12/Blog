import React, { useEffect, useState } from 'react';
import {
  Box, Typography, Container, Grid, Card, CardContent, CardActions,
  Button, TextField, Dialog, DialogActions, DialogContent, DialogTitle
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/v1';

const BlogPage = () => {
  const [blogs, setBlogs] = useState([]);
  const [myBlogs, setMyBlogs] = useState([]);
  const [newBlogDialog, setNewBlogDialog] = useState(false);
  const [blogForm, setBlogForm] = useState({ title: '', content: '' });
  const token = localStorage.getItem('token');
  const navigate = useNavigate();

  const fetchAllBlogs = async () => {
    const res = await axios.get(`${API_URL}/blogs`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setBlogs(res.data);
  };

  const fetchMyBlogs = async () => {
    const res = await axios.get(`${API_URL}/my-blogs`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setMyBlogs(res.data);
  };

  const createBlog = async () => {
    await axios.post(`${API_URL}/blogs`, blogForm, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setNewBlogDialog(false);
    setBlogForm({ title: '', content: '' });
    fetchAllBlogs();
    fetchMyBlogs();
  };

  useEffect(() => {
    if (token) {
      fetchAllBlogs();
      fetchMyBlogs();
    }
  }, []);

  return (
    <Container sx={{ mt: 6 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Explore All Blogs</Typography>
        <Button variant="contained" onClick={() => setNewBlogDialog(true)}>+ New Blog</Button>
      </Box>

      <Grid container spacing={3}>
        {blogs.map((blog) => (
          <Grid item xs={12} sm={6} md={4} key={blog.id}>
            <Card sx={{ cursor: 'pointer' }} onClick={() => navigate(`/blogs/${blog.id}`)}>
              <CardContent>
                <Typography variant="h6">{blog.title}</Typography>
                <Typography variant="body2" mt={1}>{blog.content.slice(0, 100)}...</Typography>
              </CardContent>
              <CardActions>
                <Typography variant="caption" ml={1}>By {blog.author_email}</Typography>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Typography variant="h5" mt={6} mb={2}>My Blogs</Typography>
      <Grid container spacing={3}>
        {myBlogs.map((blog) => (
          <Grid item xs={12} sm={6} md={4} key={blog.id}>
            <Card sx={{ border: '2px solid #4caf50', cursor: 'pointer' }} onClick={() => navigate(`/blogs/${blog.id}`)}>
              <CardContent>
                <Typography variant="h6">{blog.title}</Typography>
                <Typography variant="body2" mt={1}>{blog.content.slice(0, 100)}...</Typography>
              </CardContent>
              <CardActions>
                <Typography variant="caption" ml={1}>You</Typography>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={newBlogDialog} onClose={() => setNewBlogDialog(false)}>
        <DialogTitle>New Blog</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Title"
            fullWidth
            variant="standard"
            value={blogForm.title}
            onChange={(e) => setBlogForm({ ...blogForm, title: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Content"
            fullWidth
            multiline
            minRows={4}
            variant="standard"
            value={blogForm.content}
            onChange={(e) => setBlogForm({ ...blogForm, content: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewBlogDialog(false)}>Cancel</Button>
          <Button onClick={createBlog}>Post</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default BlogPage;
