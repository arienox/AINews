export interface Article {
  id: number;
  title: string;
  url: string;
  source: string;
  summary: string;
  category: string;
  priority: 'High' | 'Low';
  key_points: string[];
  action_items: string[];
  date_published: string;
  date_found: string;
  is_archived: boolean;
  is_saved?: boolean;
}

export interface ArticleWithInteractions extends Article {
  interaction_count: number;
  save_count: number;
  click_count: number;
} 