"""Script to generate an expanded Amazon bestsellers dataset (~550 books)."""
import csv
import random
import os

random.seed(42)

# Real authors by genre
fiction_authors = [
    "Stephen King", "J.K. Rowling", "Dan Brown", "John Grisham", "James Patterson",
    "Suzanne Collins", "Veronica Roth", "Gillian Flynn", "Paula Hawkins", "Delia Owens",
    "Celeste Ng", "Kristin Hannah", "Colleen Hoover", "Lisa Wingate", "Amor Towles",
    "Madeline Miller", "Donna Tartt", "Anthony Doerr", "Andy Weir", "Ernest Cline",
    "Margaret Atwood", "Khaled Hosseini", "Erin Morgenstern", "Liane Moriarty",
    "Fredrik Backman", "Dav Pilkey", "Jeff Kinney", "Rick Riordan", "Tomi Adeyemi",
    "Angie Thomas", "Brit Bennett", "Taylor Jenkins Reid", "Emily Henry",
    "Sally Rooney", "Colson Whitehead", "George Saunders", "Jesmyn Ward",
    "Lauren Groff", "Ann Patchett", "Michael Connelly", "Lee Child",
    "Nora Roberts", "Nicholas Sparks", "Janet Evanovich", "Harlan Coben",
    "David Baldacci", "Clive Cussler", "Tom Clancy", "Dean Koontz",
    "Neil Gaiman", "Brandon Sanderson", "Patrick Rothfuss", "Sarah J. Maas",
    "Leigh Bardugo", "V.E. Schwab", "Holly Black", "Cassandra Clare",
    "Rick Riordan", "R.J. Palacio", "Jason Reynolds", "Becky Albertalli",
    "Rainbow Rowell", "Jenny Han", "Nicola Yoon", "Adam Silvera",
    "Markus Zusak", "John Green", "Lois Lowry", "James Dashner",
    "Marie Lu", "Veronica Roth", "Ransom Riggs", "Marissa Meyer",
    "Stephanie Meyer", "E.L. James", "Diana Gabaldon", "Sarah Dessen",
    "Jennifer Egan", "Zadie Smith", "Chimamanda Ngozi Adichie", "Celeste Ng",
    "Tara Westover", "Heather Morris", "Kate Quinn", "Pam Jenoff",
    "Lisa See", "Min Jin Lee", "Viet Thanh Nguyen", "Hanya Yanagihara",
    "Mohsin Hamid", "Naomi Alderman", "M.L. Stedman", "Liane Moriarty",
    "Big Little Lies", "Rachel Hollis", "Dav Pilkey", "Jeff Kinney"
]

nonfiction_authors = [
    "Michelle Obama", "Barack Obama", "Malcolm Gladwell", "Yuval Noah Harari",
    "Brene Brown", "Mark Manson", "James Clear", "Jen Sincero", "Marie Kondo",
    "Rachel Hollis", "Tara Westover", "Matthew Walker", "Bill Bryson",
    "Walter Isaacson", "David McCullough", "Erik Larson", "Ron Chernow",
    "Jon Krakauer", "Laura Hillenbrand", "Rebecca Skloot", "Siddhartha Mukherjee",
    "Paul Kalanithi", "Atul Gawande", "Cheryl Strayed", "Elizabeth Gilbert",
    "Glennon Doyle", "Ibram X. Kendi", "Robin DiAngelo", "Ta-Nehisi Coates",
    "Isabel Wilkerson", "Bob Woodward", "Michael Wolff", "Mary Trump",
    "John Bolton", "Sally Yates", "Ronan Farrow", "Rachel Maddow",
    "Jordan Peterson", "Tim Ferriss", "Gary Vaynerchuk", "Simon Sinek",
    "Adam Grant", "Daniel Kahneman", "Nassim Nicholas Taleb", "Ray Dalio",
    "Tony Robbins", "Dave Ramsey", "Robert Kiyosaki", "Suze Orman",
    "Phil Knight", "Howard Schultz", "Sheryl Sandberg", "Eric Schmidt",
    "Peter Thiel", "Ben Horowitz", "Reed Hastings", "Satya Nadella",
    "Stephen Hawking", "Neil deGrasse Tyson", "Michio Kaku", "Carlo Rovelli",
    "Yuval Noah Harari", "Jared Diamond", "Steven Pinker", "Sam Harris",
    "Deepak Chopra", "Eckhart Tolle", "Thich Nhat Hanh", "Dalai Lama",
    "Dale Carnegie", "Napoleon Hill", "Stephen R. Covey", "Don Miguel Ruiz",
    "Rhonda Byrne", "Paulo Coelho", "Oprah Winfrey", "Trevor Noah",
    "Tina Fey", "Amy Poehler", "Mindy Kaling", "Kevin Hart",
    "David Goggins", "Jocko Willink", "Matthew McConaughey", "Will Smith",
    "Roxane Gay", "Maggie Nelson", "Patti Smith", "Joan Didion"
]

fiction_title_parts = {
    "starts": ["The", "A", "All the", "Before", "After", "Where", "When", "Little",
               "Big", "Dark", "Light", "Silent", "Last", "First", "Lost", "Hidden",
               "Secret", "Broken", "Forgotten", "Midnight", "Shadow", "Golden"],
    "middles": ["Fire", "Water", "Night", "Day", "Storm", "Dream", "Garden", "House",
                "Girl", "Boy", "Woman", "Man", "King", "Queen", "Wolf", "Rose",
                "Star", "Moon", "Sun", "River", "Forest", "Mountain", "Ocean",
                "Bridge", "Tower", "Castle", "Door", "Window", "Mirror", "Clock"],
    "ends": ["of Lies", "of Truth", "of Secrets", "in the Dark", "at Midnight",
             "in Winter", "in Summer", "of the Heart", "of the World", "of Fire",
             "of Ice", "of Light", "of Shadows", "of Dreams", "on the Hill",
             "by the Sea", "in the Woods", "of the Lost", "of the Fallen", "Reborn"]
}

nonfiction_title_parts = {
    "starts": ["The Art of", "The Power of", "How to", "Why We", "Think", "Becoming",
               "Dare to", "The Secret of", "Atomic", "Deep", "The Courage to",
               "Grit:", "Mindset:", "Drive:", "Flow:", "Peak:", "Range:", "Outliers:",
               "The Subtle Art of", "The 7 Rules of", "12 Rules for", "The 5 AM",
               "The Infinite", "Start with", "Leaders Eat", "Good to", "Built to",
               "From Zero to", "The Hard Thing About", "Measure What"],
    "middles": ["Habits", "Leadership", "Success", "Growth", "Focus", "Resilience",
                "Creativity", "Innovation", "Mindfulness", "Influence", "Purpose",
                "Discipline", "Strategy", "Thinking", "Learning", "Communication",
                "Persuasion", "Negotiation", "Excellence", "Mastery"],
    "ends": ["That Last", "for Life", "in Action", "Unleashed", "Redefined",
             "Revolution", "Transformed", "Decoded", "Simplified", "Matters"]
}

def generate_fiction_title():
    start = random.choice(fiction_title_parts["starts"])
    middle = random.choice(fiction_title_parts["middles"])
    if random.random() > 0.5:
        end = random.choice(fiction_title_parts["ends"])
        return f"{start} {middle} {end}"
    return f"{start} {middle}"

def generate_nonfiction_title():
    start = random.choice(nonfiction_title_parts["starts"])
    if random.random() > 0.4:
        middle = random.choice(nonfiction_title_parts["middles"])
        if random.random() > 0.5:
            end = random.choice(nonfiction_title_parts["ends"])
            return f"{start} {middle} {end}"
        return f"{start} {middle}"
    return f"{start} {random.choice(nonfiction_title_parts['middles'])}"

# Known real bestsellers to include
real_books = [
    ("Where the Crawdads Sing", "Delia Owens", 4.8, 87841, 14, 2019, "Fiction"),
    ("Becoming", "Michelle Obama", 4.7, 61133, 11, 2019, "Non Fiction"),
    ("Educated: A Memoir", "Tara Westover", 4.8, 38122, 13, 2018, "Non Fiction"),
    ("The Subtle Art of Not Giving a F*ck", "Mark Manson", 4.6, 71817, 13, 2017, "Non Fiction"),
    ("The Hunger Games", "Suzanne Collins", 4.7, 167963, 10, 2009, "Fiction"),
    ("Catching Fire", "Suzanne Collins", 4.7, 110287, 11, 2009, "Fiction"),
    ("Mockingjay", "Suzanne Collins", 4.6, 95831, 12, 2010, "Fiction"),
    ("Gone Girl", "Gillian Flynn", 4.2, 109345, 15, 2012, "Fiction"),
    ("The Fault in Our Stars", "John Green", 4.7, 113335, 12, 2012, "Fiction"),
    ("The Girl on the Train", "Paula Hawkins", 4.1, 87234, 14, 2015, "Fiction"),
    ("The Martian", "Andy Weir", 4.7, 105645, 12, 2014, "Fiction"),
    ("Ready Player One", "Ernest Cline", 4.6, 76842, 14, 2011, "Fiction"),
    ("Sapiens", "Yuval Noah Harari", 4.6, 91823, 15, 2015, "Non Fiction"),
    ("Atomic Habits", "James Clear", 4.8, 125000, 11, 2018, "Non Fiction"),
    ("The 7 Habits of Highly Effective People", "Stephen R. Covey", 4.7, 67834, 13, 2004, "Non Fiction"),
    ("Thinking, Fast and Slow", "Daniel Kahneman", 4.5, 54321, 16, 2011, "Non Fiction"),
    ("Outliers", "Malcolm Gladwell", 4.6, 78234, 14, 2008, "Non Fiction"),
    ("The Tipping Point", "Malcolm Gladwell", 4.5, 51234, 13, 2006, "Non Fiction"),
    ("Blink", "Malcolm Gladwell", 4.4, 42345, 14, 2007, "Non Fiction"),
    ("Steve Jobs", "Walter Isaacson", 4.6, 39821, 16, 2011, "Non Fiction"),
    ("Shoe Dog", "Phil Knight", 4.8, 67234, 14, 2016, "Non Fiction"),
    ("Lean In", "Sheryl Sandberg", 4.3, 31234, 15, 2013, "Non Fiction"),
    ("Born a Crime", "Trevor Noah", 4.8, 55678, 13, 2016, "Non Fiction"),
    ("Unbroken", "Laura Hillenbrand", 4.8, 88776, 15, 2010, "Non Fiction"),
    ("Hillbilly Elegy", "J.D. Vance", 4.3, 34567, 14, 2016, "Non Fiction"),
    ("The Glass Castle", "Jeannette Walls", 4.7, 76534, 12, 2005, "Non Fiction"),
    ("Wild: From Lost to Found", "Cheryl Strayed", 4.4, 63422, 13, 2012, "Non Fiction"),
    ("The Nightingale", "Kristin Hannah", 4.8, 98271, 15, 2015, "Fiction"),
    ("All the Light We Cannot See", "Anthony Doerr", 4.6, 103921, 15, 2014, "Fiction"),
    ("Big Little Lies", "Liane Moriarty", 4.5, 67234, 14, 2014, "Fiction"),
    ("The Goldfinch", "Donna Tartt", 4.0, 26921, 18, 2013, "Fiction"),
    ("A Man Called Ove", "Fredrik Backman", 4.7, 78234, 13, 2014, "Fiction"),
    ("The Kite Runner", "Khaled Hosseini", 4.6, 86541, 11, 2003, "Fiction"),
    ("The Book Thief", "Markus Zusak", 4.7, 60979, 11, 2007, "Fiction"),
    ("Divergent", "Veronica Roth", 4.6, 75671, 10, 2011, "Fiction"),
    ("The Maze Runner", "James Dashner", 4.6, 67347, 11, 2014, "Fiction"),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 4.9, 120000, 10, 2001, "Fiction"),
    ("Harry Potter and the Chamber of Secrets", "J.K. Rowling", 4.8, 98000, 10, 2002, "Fiction"),
    ("Harry Potter and the Prisoner of Azkaban", "J.K. Rowling", 4.9, 105000, 11, 2003, "Fiction"),
    ("Harry Potter and the Goblet of Fire", "J.K. Rowling", 4.8, 95000, 12, 2004, "Fiction"),
    ("Harry Potter and the Order of the Phoenix", "J.K. Rowling", 4.7, 88000, 13, 2005, "Fiction"),
    ("Harry Potter and the Half-Blood Prince", "J.K. Rowling", 4.8, 92000, 12, 2006, "Fiction"),
    ("Harry Potter and the Deathly Hallows", "J.K. Rowling", 4.8, 110000, 14, 2007, "Fiction"),
    ("The Da Vinci Code", "Dan Brown", 4.3, 145000, 15, 2003, "Fiction"),
    ("Angels and Demons", "Dan Brown", 4.4, 87000, 14, 2004, "Fiction"),
    ("Inferno", "Dan Brown", 4.2, 65000, 16, 2013, "Fiction"),
    ("Origin", "Dan Brown", 4.1, 45000, 17, 2017, "Fiction"),
    ("It Ends with Us", "Colleen Hoover", 4.6, 134000, 13, 2016, "Fiction"),
    ("Verity", "Colleen Hoover", 4.5, 98000, 14, 2018, "Fiction"),
    ("Ugly Love", "Colleen Hoover", 4.4, 67000, 12, 2014, "Fiction"),
    ("November 9", "Colleen Hoover", 4.5, 54000, 13, 2015, "Fiction"),
    ("Confess", "Colleen Hoover", 4.4, 43000, 12, 2015, "Fiction"),
    ("Circe", "Madeline Miller", 4.6, 33921, 16, 2018, "Fiction"),
    ("The Song of Achilles", "Madeline Miller", 4.7, 67000, 14, 2012, "Fiction"),
    ("Eleanor Oliphant Is Completely Fine", "Gail Honeyman", 4.6, 47921, 15, 2017, "Fiction"),
    ("The Silent Patient", "Alex Michaelides", 4.3, 87000, 14, 2019, "Fiction"),
    ("Daisy Jones & The Six", "Taylor Jenkins Reid", 4.4, 56000, 15, 2019, "Fiction"),
    ("The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", 4.6, 98000, 14, 2017, "Fiction"),
    ("Malibu Rising", "Taylor Jenkins Reid", 4.3, 34000, 16, 2021, "Fiction"),
    ("Beach Read", "Emily Henry", 4.3, 67000, 14, 2020, "Fiction"),
    ("People We Meet on Vacation", "Emily Henry", 4.4, 78000, 15, 2021, "Fiction"),
    ("Book Lovers", "Emily Henry", 4.3, 56000, 15, 2022, "Fiction"),
    ("Normal People", "Sally Rooney", 4.1, 45000, 14, 2019, "Fiction"),
    ("Beautiful World Where Are You", "Sally Rooney", 3.8, 34000, 16, 2021, "Fiction"),
    ("The Vanishing Half", "Brit Bennett", 4.4, 67000, 15, 2020, "Fiction"),
    ("Mexican Gothic", "Silvia Moreno-Garcia", 4.1, 34000, 14, 2020, "Fiction"),
    ("The Midnight Library", "Matt Haig", 4.3, 87000, 14, 2020, "Fiction"),
    ("Project Hail Mary", "Andy Weir", 4.8, 98000, 15, 2021, "Fiction"),
    ("Klara and the Sun", "Kazuo Ishiguro", 4.1, 34000, 16, 2021, "Fiction"),
    ("The Invisible Life of Addie LaRue", "V.E. Schwab", 4.5, 67000, 15, 2020, "Fiction"),
    ("A Court of Thorns and Roses", "Sarah J. Maas", 4.5, 145000, 13, 2015, "Fiction"),
    ("A Court of Mist and Fury", "Sarah J. Maas", 4.7, 134000, 14, 2016, "Fiction"),
    ("A Court of Wings and Ruin", "Sarah J. Maas", 4.6, 98000, 15, 2017, "Fiction"),
    ("Throne of Glass", "Sarah J. Maas", 4.4, 87000, 12, 2012, "Fiction"),
    ("Six of Crows", "Leigh Bardugo", 4.6, 78000, 13, 2015, "Fiction"),
    ("Ninth House", "Leigh Bardugo", 4.3, 34000, 16, 2019, "Fiction"),
    ("Children of Blood and Bone", "Tomi Adeyemi", 4.5, 56000, 14, 2018, "Fiction"),
    ("The Hate U Give", "Angie Thomas", 4.7, 78000, 13, 2017, "Fiction"),
    ("Wonder", "R.J. Palacio", 4.8, 98000, 12, 2012, "Fiction"),
    ("Diary of a Wimpy Kid", "Jeff Kinney", 4.7, 67000, 10, 2007, "Fiction"),
    ("Diary of a Wimpy Kid: Rodrick Rules", "Jeff Kinney", 4.7, 45000, 10, 2008, "Fiction"),
    ("Diary of a Wimpy Kid: The Last Straw", "Jeff Kinney", 4.6, 43000, 10, 2009, "Fiction"),
    ("Dog Man", "Dav Pilkey", 4.9, 45000, 8, 2016, "Fiction"),
    ("Dog Man: Unleashed", "Dav Pilkey", 4.9, 34000, 8, 2017, "Fiction"),
    ("Captain Underpants", "Dav Pilkey", 4.8, 56000, 9, 2013, "Fiction"),
    ("Percy Jackson: The Lightning Thief", "Rick Riordan", 4.7, 87000, 11, 2005, "Fiction"),
    ("Percy Jackson: Sea of Monsters", "Rick Riordan", 4.6, 67000, 11, 2006, "Fiction"),
    ("Percy Jackson: The Titan's Curse", "Rick Riordan", 4.7, 56000, 11, 2007, "Fiction"),
    ("The Alchemist", "Paulo Coelho", 4.7, 134000, 12, 2006, "Fiction"),
    ("Life of Pi", "Yann Martel", 4.3, 36889, 11, 2002, "Fiction"),
    ("The Help", "Kathryn Stockett", 4.8, 87841, 15, 2011, "Fiction"),
    ("The Girl with the Dragon Tattoo", "Stieg Larsson", 4.5, 67000, 14, 2009, "Fiction"),
    ("The Handmaid's Tale", "Margaret Atwood", 4.3, 98271, 14, 2017, "Fiction"),
    ("1984", "George Orwell", 4.7, 145000, 10, 2017, "Fiction"),
    ("To Kill a Mockingbird", "Harper Lee", 4.8, 167000, 11, 2015, "Fiction"),
    ("Think and Grow Rich", "Napoleon Hill", 4.7, 43289, 10, 2010, "Non Fiction"),
    ("How to Win Friends and Influence People", "Dale Carnegie", 4.7, 71238, 11, 2009, "Non Fiction"),
    ("The Power of Now", "Eckhart Tolle", 4.6, 34829, 12, 2004, "Non Fiction"),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", 4.6, 98000, 11, 2006, "Non Fiction"),
    ("The 4-Hour Workweek", "Tim Ferriss", 4.4, 45000, 15, 2007, "Non Fiction"),
    ("Tools of Titans", "Tim Ferriss", 4.5, 34000, 18, 2016, "Non Fiction"),
    ("Tribe of Mentors", "Tim Ferriss", 4.3, 23000, 19, 2017, "Non Fiction"),
    ("Start with Why", "Simon Sinek", 4.6, 67000, 14, 2009, "Non Fiction"),
    ("Leaders Eat Last", "Simon Sinek", 4.6, 45000, 15, 2014, "Non Fiction"),
    ("The Infinite Game", "Simon Sinek", 4.5, 34000, 16, 2019, "Non Fiction"),
    ("Dare to Lead", "Brene Brown", 4.7, 56000, 15, 2018, "Non Fiction"),
    ("Daring Greatly", "Brene Brown", 4.7, 45000, 14, 2012, "Non Fiction"),
    ("The Gifts of Imperfection", "Brene Brown", 4.7, 34000, 13, 2010, "Non Fiction"),
    ("You Are a Badass", "Jen Sincero", 4.6, 54912, 13, 2013, "Non Fiction"),
    ("You Are a Badass at Making Money", "Jen Sincero", 4.5, 23000, 14, 2017, "Non Fiction"),
    ("Girl Wash Your Face", "Rachel Hollis", 4.3, 67000, 14, 2018, "Non Fiction"),
    ("Girl Stop Apologizing", "Rachel Hollis", 4.4, 34000, 15, 2019, "Non Fiction"),
    ("Untamed", "Glennon Doyle", 4.6, 78000, 14, 2020, "Non Fiction"),
    ("The Life-Changing Magic of Tidying Up", "Marie Kondo", 4.5, 47829, 14, 2014, "Non Fiction"),
    ("Spark Joy", "Marie Kondo", 4.4, 23000, 15, 2016, "Non Fiction"),
    ("Why We Sleep", "Matthew Walker", 4.6, 56000, 15, 2017, "Non Fiction"),
    ("A Brief History of Time", "Stephen Hawking", 4.7, 78000, 14, 2005, "Non Fiction"),
    ("The Theory of Everything", "Stephen Hawking", 4.5, 23000, 13, 2006, "Non Fiction"),
    ("Astrophysics for People in a Hurry", "Neil deGrasse Tyson", 4.4, 45000, 14, 2017, "Non Fiction"),
    ("Cosmos", "Neil deGrasse Tyson", 4.6, 34000, 15, 2014, "Non Fiction"),
    ("Homo Deus", "Yuval Noah Harari", 4.5, 31289, 16, 2017, "Non Fiction"),
    ("21 Lessons for the 21st Century", "Yuval Noah Harari", 4.4, 24378, 17, 2018, "Non Fiction"),
    ("The Immortal Life of Henrietta Lacks", "Rebecca Skloot", 4.7, 38291, 13, 2010, "Non Fiction"),
    ("When Breath Becomes Air", "Paul Kalanithi", 4.8, 56722, 14, 2016, "Non Fiction"),
    ("Being Mortal", "Atul Gawande", 4.7, 25689, 15, 2014, "Non Fiction"),
    ("The Emperor of All Maladies", "Siddhartha Mukherjee", 4.6, 11827, 17, 2010, "Non Fiction"),
    ("Elon Musk", "Ashlee Vance", 4.6, 27834, 15, 2015, "Non Fiction"),
    ("Leonardo da Vinci", "Walter Isaacson", 4.5, 14782, 18, 2017, "Non Fiction"),
    ("Alexander Hamilton", "Ron Chernow", 4.7, 20961, 16, 2004, "Non Fiction"),
    ("Into Thin Air", "Jon Krakauer", 4.6, 28944, 14, 2004, "Non Fiction"),
    ("Into the Wild", "Jon Krakauer", 4.5, 45000, 13, 2007, "Non Fiction"),
    ("The Boys in the Boat", "Daniel James Brown", 4.8, 44829, 14, 2013, "Non Fiction"),
    ("Hidden Figures", "Margot Lee Shetterly", 4.7, 27814, 13, 2016, "Non Fiction"),
    ("The Devil in the White City", "Erik Larson", 4.3, 31829, 15, 2003, "Non Fiction"),
    ("Dead Wake", "Erik Larson", 4.4, 23000, 16, 2015, "Non Fiction"),
    ("In the Garden of Beasts", "Erik Larson", 4.3, 19000, 15, 2011, "Non Fiction"),
    ("Killers of the Flower Moon", "David Grann", 4.6, 56000, 16, 2017, "Non Fiction"),
    ("Fear: Trump in the White House", "Bob Woodward", 4.0, 13829, 19, 2018, "Non Fiction"),
    ("Rage", "Bob Woodward", 4.1, 23000, 18, 2020, "Non Fiction"),
    ("Fire and Fury", "Michael Wolff", 3.9, 34000, 17, 2018, "Non Fiction"),
    ("Too Much and Never Enough", "Mary Trump", 4.1, 45000, 16, 2020, "Non Fiction"),
    ("A Promised Land", "Barack Obama", 4.8, 87000, 18, 2020, "Non Fiction"),
    ("Greenlights", "Matthew McConaughey", 4.5, 56000, 15, 2020, "Non Fiction"),
    ("Will", "Will Smith", 4.6, 45000, 16, 2021, "Non Fiction"),
    ("Can't Hurt Me", "David Goggins", 4.8, 98000, 14, 2018, "Non Fiction"),
    ("Never Finished", "David Goggins", 4.8, 34000, 16, 2022, "Non Fiction"),
    ("Extreme Ownership", "Jocko Willink", 4.7, 45000, 15, 2015, "Non Fiction"),
    ("The 48 Laws of Power", "Robert Greene", 4.6, 56000, 16, 2009, "Non Fiction"),
    ("The Art of War", "Sun Tzu", 4.5, 34000, 10, 2007, "Non Fiction"),
    ("Quiet", "Susan Cain", 4.5, 45000, 14, 2012, "Non Fiction"),
    ("Grit", "Angela Duckworth", 4.5, 34000, 15, 2016, "Non Fiction"),
    ("Mindset", "Carol Dweck", 4.6, 56000, 14, 2008, "Non Fiction"),
    ("Drive", "Daniel H. Pink", 4.4, 23000, 15, 2009, "Non Fiction"),
    ("The Lean Startup", "Eric Ries", 4.5, 34000, 16, 2011, "Non Fiction"),
    ("Zero to One", "Peter Thiel", 4.5, 45000, 15, 2014, "Non Fiction"),
    ("The Hard Thing About Hard Things", "Ben Horowitz", 4.6, 23000, 17, 2014, "Non Fiction"),
    ("Principles", "Ray Dalio", 4.5, 34000, 18, 2017, "Non Fiction"),
    ("Good to Great", "Jim Collins", 4.5, 45000, 16, 2006, "Non Fiction"),
    ("Built to Last", "Jim Collins", 4.4, 23000, 17, 2007, "Non Fiction"),
    ("12 Rules for Life", "Jordan Peterson", 4.5, 67000, 16, 2018, "Non Fiction"),
    ("How to Be an Antiracist", "Ibram X. Kendi", 4.4, 45000, 15, 2019, "Non Fiction"),
    ("White Fragility", "Robin DiAngelo", 4.0, 56000, 14, 2018, "Non Fiction"),
    ("Between the World and Me", "Ta-Nehisi Coates", 4.5, 34000, 13, 2015, "Non Fiction"),
    ("Caste", "Isabel Wilkerson", 4.6, 45000, 16, 2020, "Non Fiction"),
    ("The Warmth of Other Suns", "Isabel Wilkerson", 4.7, 34000, 15, 2010, "Non Fiction"),
    ("Talking to Strangers", "Malcolm Gladwell", 4.3, 34000, 16, 2019, "Non Fiction"),
    ("David and Goliath", "Malcolm Gladwell", 4.4, 28000, 15, 2013, "Non Fiction"),
    ("Man's Search for Meaning", "Viktor Frankl", 4.7, 98000, 10, 2006, "Non Fiction"),
    ("The Four Agreements", "Don Miguel Ruiz", 4.7, 31829, 11, 2005, "Non Fiction"),
    ("The Secret", "Rhonda Byrne", 4.3, 56000, 12, 2006, "Non Fiction"),
    ("Eat Pray Love", "Elizabeth Gilbert", 4.2, 45000, 14, 2006, "Non Fiction"),
    ("Big Magic", "Elizabeth Gilbert", 4.4, 23000, 13, 2015, "Non Fiction"),
    ("Bossypants", "Tina Fey", 4.3, 34000, 13, 2011, "Non Fiction"),
    ("Yes Please", "Amy Poehler", 4.2, 23000, 14, 2014, "Non Fiction"),
    ("Is Everyone Hanging Out Without Me?", "Mindy Kaling", 4.3, 23000, 13, 2011, "Non Fiction"),
]

# Generate additional books to reach ~550
generated_books = []
used_titles = set(book[0] for book in real_books)
years = list(range(2001, 2023))

while len(real_books) + len(generated_books) < 550:
    genre = random.choice(["Fiction", "Non Fiction"])
    
    if genre == "Fiction":
        title = generate_fiction_title()
        author = random.choice(fiction_authors)
    else:
        title = generate_nonfiction_title()
        author = random.choice(nonfiction_authors)
    
    if title in used_titles:
        continue
    used_titles.add(title)
    
    year = random.choice(years)
    
    # Rating distribution: mostly 3.8-4.9
    rating = round(random.triangular(3.5, 5.0, 4.5), 1)
    rating = min(4.9, max(3.5, rating))
    
    # Reviews: log-normal-ish
    reviews = int(random.lognormvariate(10, 1.2))
    reviews = min(180000, max(1000, reviews))
    
    # Price: 8-25
    price = random.randint(8, 25)
    
    generated_books.append((title, author, rating, reviews, price, year, genre))

all_books = real_books + generated_books
random.shuffle(all_books)

output_path = os.path.join(os.path.dirname(__file__), "data", "amazon_bestsellers.csv")
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Author", "User Rating", "Reviews", "Price", "Year", "Genre"])
    for book in all_books:
        writer.writerow(book)

print(f"Generated {len(all_books)} books -> {output_path}")
