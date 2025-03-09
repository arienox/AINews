import React, { useState } from 'react';
import {
  Grid,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  SelectChangeEvent,
  Pagination
} from '@mui/material';
import ArticleCard from './ArticleCard';
import { Article } from '../../types/article';

interface ArticleListProps {
  articles: Article[];
  onSave: (articleId: number) => void;
  onShare: (articleId: number) => void;
  onOpen: (articleId: number) => void;
}

const ArticleList: React.FC<ArticleListProps> = ({
  articles,
  onSave,
  onShare,
  onOpen
}) => {
  const [category, setCategory] = useState<string>('all');
  const [priority, setPriority] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [page, setPage] = useState(1);
  const articlesPerPage = 12;

  const handleCategoryChange = (event: SelectChangeEvent) => {
    setCategory(event.target.value);
    setPage(1);
  };

  const handlePriorityChange = (event: SelectChangeEvent) => {
    setPriority(event.target.value);
    setPage(1);
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
    setPage(1);
  };

  const filteredArticles = articles.filter((article) => {
    const matchesCategory = category === 'all' || article.category === category;
    const matchesPriority = priority === 'all' || article.priority === priority;
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         article.summary.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesCategory && matchesPriority && matchesSearch;
  });

  const paginatedArticles = filteredArticles.slice(
    (page - 1) * articlesPerPage,
    page * articlesPerPage
  );

  const pageCount = Math.ceil(filteredArticles.length / articlesPerPage);

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Category</InputLabel>
          <Select
            value={category}
            label="Category"
            onChange={handleCategoryChange}
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="Models/Agents">Models/Agents</MenuItem>
            <MenuItem value="Tools">Tools</MenuItem>
            <MenuItem value="Research">Research</MenuItem>
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Priority</InputLabel>
          <Select
            value={priority}
            label="Priority"
            onChange={handlePriorityChange}
          >
            <MenuItem value="all">All</MenuItem>
            <MenuItem value="High">High</MenuItem>
            <MenuItem value="Low">Low</MenuItem>
          </Select>
        </FormControl>

        <TextField
          label="Search"
          variant="outlined"
          value={searchQuery}
          onChange={handleSearchChange}
          sx={{ flexGrow: 1 }}
        />
      </Box>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        {paginatedArticles.map((article) => (
          <Grid item xs={12} sm={6} md={4} key={article.id}>
            <ArticleCard
              article={article}
              onSave={onSave}
              onShare={onShare}
              onOpen={onOpen}
            />
          </Grid>
        ))}
      </Grid>

      {pageCount > 1 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Pagination
            count={pageCount}
            page={page}
            onChange={(_, value) => setPage(value)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
};

export default ArticleList; 