import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { BookOpen, Star, DollarSign, MessageSquare } from 'lucide-react';

const SummaryCards = ({ summary }) => {
  if (!summary) return null;

  const cards = [
    {
      title: 'Total Books',
      value: summary.total_books.toLocaleString(),
      icon: BookOpen,
      color: 'text-[#EA580C]',
      bgColor: 'bg-orange-50',
      testId: 'total-books-card'
    },
    {
      title: 'Avg Rating',
      value: summary.avg_rating.toFixed(2),
      icon: Star,
      color: 'text-[#2563EB]',
      bgColor: 'bg-blue-50',
      testId: 'avg-rating-card'
    },
    {
      title: 'Avg Price',
      value: `$${summary.avg_price.toFixed(2)}`,
      icon: DollarSign,
      color: 'text-[#10B981]',
      bgColor: 'bg-green-50',
      testId: 'avg-price-card'
    },
    {
      title: 'Total Reviews',
      value: summary.total_reviews.toLocaleString(),
      icon: MessageSquare,
      color: 'text-[#F59E0B]',
      bgColor: 'bg-yellow-50',
      testId: 'total-reviews-card'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
      {cards.map((card, index) => {
        const Icon = card.icon;
        return (
          <Card key={index} data-testid={card.testId} className="card-hover bg-white border border-[#E5E7EB] rounded-lg shadow-sm">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-widest font-semibold text-[#4B5563] mb-2">
                    {card.title}
                  </p>
                  <p className="text-3xl font-black text-[#030712] tracking-tight">
                    {card.value}
                  </p>
                </div>
                <div className={`${card.bgColor} ${card.color} p-3 rounded-lg`}>
                  <Icon className="h-7 w-7" strokeWidth={1.5} />
                </div>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};

export default SummaryCards;
