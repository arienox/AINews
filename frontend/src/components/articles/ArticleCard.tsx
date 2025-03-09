import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  Box,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Bookmark,
  BookmarkBorder,
  Share,
  OpenInNew
} from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';

interface Article {
  id: number;
  title: string;
  url: string;
  source: string;
  summary: string;
  category: string;
  priority: 'High' | 'Low';
  date_published: string;
  is_saved?: boolean;
}

interface ArticleCardProps {
  article: Article;
  onSave: (articleId: number) => void;
  onShare: (articleId: number) => void;
  onOpen: (articleId: number) => void;
}

const ArticleCard: React.FC<ArticleCardProps> = ({
  article,
  onSave,
  onShare,
  onOpen
}) => {
  const getPriorityColor = (priority: string) => {
    return priority === 'High' ? 'error' : 'default';
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Models/Agents':
        return 'primary';
      case 'Tools':
        return 'success';
      case 'Research':
        return 'secondary';
      default:
        return 'default';
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
          <Chip
            label={article.category}
            size="small"
            color={getCategoryColor(article.category)}
          />
          <Chip
            label={article.priority}
            size="small"
            color={getPriorityColor(article.priority)}
          />
        </Box>
        
        <Typography variant="h6" component="h2" gutterBottom>
          {article.title}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          {article.summary.length > 150
            ? `${article.summary.substring(0, 150)}...`
            : article.summary}
        </Typography>
        
        <Typography variant="caption" color="text.secondary">
          {article.source} • {formatDistanceToNow(new Date(article.date_published))} ago
        </Typography>
      </CardContent>
      
      <CardActions>
        <Tooltip title={article.is_saved ? "Unsave article" : "Save article"}>
          <IconButton onClick={() => onSave(article.id)}>
            {article.is_saved ? <Bookmark /> : <BookmarkBorder />}
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Share article">
          <IconButton onClick={() => onShare(article.id)}>
            <Share />
          </IconButton>
        </Tooltip>
        
        <Box sx={{ flexGrow: 1 }} />
        
        <Button
          size="small"
          endIcon={<OpenInNew />}
          onClick={() => onOpen(article.id)}
        >
          Read More
        </Button>
      </CardActions>
    </Card>
  );
};

export default ArticleCard; 