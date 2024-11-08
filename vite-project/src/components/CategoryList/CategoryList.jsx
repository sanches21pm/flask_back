// CategoryList.jsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Container,
  CircularProgress,
  Alert,
} from '@mui/material';

const CategoryList = () => {
  const [categories, setCategories] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    axios
      .get('/categories') // Adjust the endpoint if necessary
      .then((response) => {
        setCategories(response.data);
      })
      .catch((error) => {
        console.error('Error fetching the categories:', error);
        setError('Failed to load categories. Please try again later.');
      });
  }, []);

  if (error) {
    return (
      <Container style={{ marginTop: '50px' }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!categories) {
    return (
      <Container style={{ textAlign: 'center', marginTop: '50px' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container style={{ marginTop: '30px' }}>
      <Typography variant="h4" gutterBottom>
        Product Categories
      </Typography>
      <Grid container spacing={4}>
        {categories.map((category) => (
          <Grid item key={category.id} xs={12} sm={6} md={4}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
            >
              <CardContent>
                <Typography gutterBottom variant="h5" component="h2">
                  {category.name}
                </Typography>
                <Typography>{category.description}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default CategoryList;
