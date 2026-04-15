import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const BooksTable = ({ selectedYear, selectedGenre }) => {
  const [books, setBooks] = useState([]);
  const [total, setTotal] = useState(0);

  const fetchBooks = async () => {
    try {
      const params = new URLSearchParams();
      if (selectedYear !== 'all') params.append('year', selectedYear);
      if (selectedGenre !== 'all') params.append('genre', selectedGenre);
      params.append('limit', '50');

      const response = await axios.get(`${API}/books?${params.toString()}`);
      setBooks(response.data.books);
      setTotal(response.data.total);
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  };

  useEffect(() => {
    fetchBooks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedYear, selectedGenre]);

  return (
    <Card data-testid="books-table" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm">
      <CardHeader className="border-b border-[#E5E7EB]">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-bold text-[#030712] tracking-tight">Books Data</CardTitle>
          <span className="text-xs bg-blue-100 text-[#2563EB] px-3 py-1 rounded-full font-semibold">
            Showing {books.length} of {total} books
          </span>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow className="bg-[#F9FAFB]">
                <TableHead className="font-semibold text-[#030712]">Name</TableHead>
                <TableHead className="font-semibold text-[#030712]">Author</TableHead>
                <TableHead className="font-semibold text-[#030712]">Rating</TableHead>
                <TableHead className="font-semibold text-[#030712]">Reviews</TableHead>
                <TableHead className="font-semibold text-[#030712]">Price</TableHead>
                <TableHead className="font-semibold text-[#030712]">Year</TableHead>
                <TableHead className="font-semibold text-[#030712]">Genre</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {books.map((book, index) => (
                <TableRow key={index} className="hover:bg-gray-50" data-testid={`book-row-${index}`}>
                  <TableCell className="font-medium text-[#030712]">{book.Name}</TableCell>
                  <TableCell className="text-[#4B5563]">{book.Author}</TableCell>
                  <TableCell className="text-[#4B5563]">
                    <span className="inline-flex items-center gap-1">
                      <span className="text-yellow-500">★</span>
                      {book['User Rating']}
                    </span>
                  </TableCell>
                  <TableCell className="text-[#4B5563]">{book.Reviews.toLocaleString()}</TableCell>
                  <TableCell className="text-[#4B5563]">${book.Price}</TableCell>
                  <TableCell className="text-[#4B5563]">{book.Year}</TableCell>
                  <TableCell>
                    <span className={`inline-block px-2 py-1 rounded-full text-xs font-semibold ${
                      book.Genre === 'Fiction' 
                        ? 'bg-orange-100 text-[#EA580C]' 
                        : 'bg-blue-100 text-[#2563EB]'
                    }`}>
                      {book.Genre}
                    </span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};

export default BooksTable;
