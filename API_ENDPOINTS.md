# ByteMap API Endpoints Documentation

This document provides a comprehensive list of all API endpoints available in the ByteMap Organization backend.

## Base URL

`/api`

---

## 1. Authentication

### **POST** `/auth/login`

Authenticates a user and returns a JWT token.

- **Request Body:**
  ```json
  {
    "username": "string",
    "pin": "string"
  }
  ```
- **Response:**
  ```json
  {
    "token": "string",
    "user": { "id": "uuid", "username": "string" }
  }
  ```

### **GET** `/auth/verify`

Verifies the current session token.

- **Headers:** `Authorization: Bearer <token>`
- **Response:** `200 OK` or `401 Unauthorized`

---

## 2. Blog

### **GET** `/blog`

Retrieves a list of blog posts.

- **Query Parameters:**
  - `category` (optional): Filter by category.
  - `featured` (optional): Set to `true` to get only featured posts.
  - `limit` (optional): Limit the number of results.

### **POST** `/blog`

Creates a new blog post.

- **Request Body:**
  ```json
  {
    "title": "string",
    "excerpt": "string",
    "content": "string",
    "category": "string",
    "author_name": "string",
    "author_initials": "string",
    "author_role": "string",
    "read_time": "string (optional)",
    "gradient": "string (optional)",
    "featured": "boolean (optional)",
    "published": "boolean (optional)"
  }
  ```

### **GET** `/blog/:slug`

Retrieves a single blog post by its slug.

### **PUT** `/blog/:slug`

Updates an existing blog post.

### **DELETE** `/blog/:slug`

Deletes a blog post.

### **GET** `/blog/categories`

Retrieves all unique blog categories.

---

## 3. Projects (Portfolio)

### **GET** `/projects`

Retrieves a list of projects.

- **Query Parameters:**
  - `category` (optional): Filter by category.
  - `featured` (optional): Set to `true` to get only featured projects.
  - `limit` (optional): Limit results.

### **POST** `/projects`

Creates a new project.

- **Request Body:**
  ```json
  {
    "title": "string",
    "category": "string",
    "description": "string",
    "long_description": "string",
    "technologies": ["string"],
    "gradient": "string",
    "metrics": "object",
    "year": "string",
    "client_name": "string",
    "live_url": "string",
    "github_url": "string (optional)"
  }
  ```

### **GET** `/projects/:slug`

Retrieves a single project by slug.

### **PUT** `/projects/:slug`

Updates a project.

### **DELETE** `/projects/:slug`

Deletes a project.

### **GET** `/projects/categories`

Retrieves all unique project categories.

---

## 4. Services

### **GET** `/services`

Retrieves all services.

### **POST** `/services`

Creates a new service.

### **GET** `/services/:id`

Retrieves a single service by ID.

### **PUT** `/services/:id`

Updates a service.

### **DELETE** `/services/:id`

Deletes a service.

---

## 5. Comments

### **GET** `/comments`

Retrieves all blog comments with post details (Admin view).

### **POST** `/comments`

Adds a new comment to a blog post.

- **Request Body:**
  ```json
  {
    "blog_post_id": "uuid",
    "author_name": "string",
    "content": "string"
  }
  ```

### **GET** `/comments/post/:blogPostId`

Retrieves all comments for a specific blog post.

### **DELETE** `/comments/:id`

Deletes a specific comment.

---

## 6. Contact Inquiries

### **GET** `/contact`

Retrieves all contact inquiries.

### **POST** `/contact`

Submits a new contact inquiry.

- **Request Body:**
  ```json
  {
    "name": "string",
    "email": "string",
    "company": "string (optional)",
    "budget": "string (optional)",
    "message": "string"
  }
  ```

### **POST** `/contact/mark-read`

Marks multiple inquiries as read.

- **Request Body:** `{ "ids": ["id1", "id2"] }`

### **PUT** `/contact/:id`

Updates inquiry status or read state.

### **DELETE** `/contact/:id`

Deletes an inquiry.

---

## 7. Media Uploads

### **POST** `/upload/:type`

Uploads a single image.

- **Path Parameter:** `type` (e.g., `blog`, `projects`, `testimonials`).
- **Body:** `FormData` with field `image`.

### **POST** `/upload/:type/multiple`

Uploads multiple images.

- **Body:** `FormData` with field `images` (array).

### **DELETE** `/upload/:type/:filename`

Deletes an uploaded file from the server.

---

## 8. Testimonials

### **GET** `/testimonials`

- **Query Parameter:** `featured=true` (optional).

### **POST** `/testimonials`

### **PUT** `/testimonials/:id`

### **DELETE** `/testimonials/:id`

---

## 9. Stats & Milestones

### **GET** `/stats`

### **POST** `/stats`

### **PUT** `/stats/:id`

### **DELETE** `/stats/:id`

### **GET** `/milestones`

### **POST** `/milestones`

### **PUT** `/milestones/:id`

### **DELETE** `/milestones/:id`

---

## 10. FAQs

### **GET** `/faqs`

### **POST** `/faqs`

### **PUT** `/faqs/:id`

### **DELETE** `/faqs/:id`

---

## 11. Health Check

### **GET** `/health`

Returns the health status of the API and database connection.

- **Response:**
  ```json
  {
    "status": "healthy",
    "database": "connected",
    "timestamp": "iso-date"
  }
  ```
