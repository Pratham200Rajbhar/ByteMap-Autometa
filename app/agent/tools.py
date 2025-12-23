import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from blogs.createBlog import create_blog as api_create_blog
from blogs.readBlog import read_blogs as api_read_blogs, read_blog_by_slug as api_read_blog_by_slug
from projects.createProject import create_project as api_create_project
from projects.readProject import read_projects as api_read_projects, read_project_by_slug as api_read_project_by_slug
from services.readService import read_services as api_read_services
from contact.readContact import read_contacts as api_read_contacts
from comments.createComment import create_comment as api_create_comment
from comments.readComment import read_comments as api_read_comments


gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)


@tool
def generate_content(prompt: str, content_type: str = "blog") -> str:
    """Generate content using Gemini AI based on the given prompt."""
    try:
        if content_type == "blog":
            system_prompt = f"""You are a professional content writer for ByteMap, a technology company.
Generate a high-quality blog post about: {prompt}

Format your response as JSON with these fields:
- title: A catchy, SEO-friendly title
- excerpt: A compelling 2-3 sentence summary
- content: Full blog content in markdown format (at least 500 words)
- category: One of: Technology, Business, Design, Development, AI, Web Development

Make the content engaging, informative, and professional."""
        
        elif content_type == "project_description":
            system_prompt = f"""Generate a professional project description for: {prompt}

Format your response as JSON with these fields:
- description: A short one-paragraph description
- long_description: A detailed 2-3 paragraph description
- technologies: An array of relevant technologies"""
        
        else:
            system_prompt = f"Generate professional content about: {prompt}"
        
        response = gemini_model.invoke([HumanMessage(content=system_prompt)])
        return response.content
    except Exception as e:
        return f"Error generating content: {str(e)}"


@tool
def create_blog_post(topic: str) -> str:
    """Generate and publish a new blog post about the given topic."""
    try:
        content_json = generate_content.invoke({"prompt": topic, "content_type": "blog"})
        
        try:
            content_json = content_json.strip()
            if content_json.startswith("```json"):
                content_json = content_json[7:]
            if content_json.startswith("```"):
                content_json = content_json[3:]
            if content_json.endswith("```"):
                content_json = content_json[:-3]
            content_data = json.loads(content_json.strip())
        except json.JSONDecodeError:
            return f"Error: Could not parse generated content. Raw response: {content_json[:200]}"
        
        result = api_create_blog(
            title=content_data.get("title", f"Blog about {topic}"),
            excerpt=content_data.get("excerpt", ""),
            content=content_data.get("content", ""),
            category=content_data.get("category", "Technology")
        )
        
        if "error" in str(result).lower():
            return f"❌ Error creating blog: {result}"
        
        return f"✅ Blog published successfully!\n📝 Title: {content_data.get('title')}\n📂 Category: {content_data.get('category')}"
    
    except Exception as e:
        return f"❌ Error creating blog: {str(e)}"


@tool
def list_all_blogs() -> str:
    """Retrieve and list all published blog posts."""
    try:
        blogs = api_read_blogs()
        
        if not blogs or len(blogs) == 0:
            return "📭 No blogs found."
        
        result = f"📚 Found {len(blogs)} blog(s):\n\n"
        for i, blog in enumerate(blogs[:10], 1):
            title = blog.get("title", "Untitled")
            category = blog.get("category", "Uncategorized")
            slug = blog.get("slug", "")
            result += f"{i}. **{title}**\n   📂 {category} | 🔗 {slug}\n\n"
        
        if len(blogs) > 10:
            result += f"...and {len(blogs) - 10} more blogs."
        
        return result
    except Exception as e:
        return f"❌ Error fetching blogs: {str(e)}"


@tool
def get_blog_details(slug: str) -> str:
    """Get details of a specific blog post by its slug."""
    try:
        blog = api_read_blog_by_slug(slug)
        
        if not blog or "error" in str(blog).lower():
            return f"❌ Blog not found with slug: {slug}"
        
        return f"""📝 **{blog.get('title', 'Untitled')}**

📂 Category: {blog.get('category', 'N/A')}
👤 Author: {blog.get('author_name', 'N/A')}
⏱️ Read time: {blog.get('read_time', 'N/A')}

📄 Excerpt:
{blog.get('excerpt', 'No excerpt available')}"""
    
    except Exception as e:
        return f"❌ Error fetching blog: {str(e)}"


@tool
def list_all_projects() -> str:
    """Retrieve and list all portfolio projects."""
    try:
        projects = api_read_projects()
        
        if not projects or len(projects) == 0:
            return "📭 No projects found."
        
        result = f"🗂️ Found {len(projects)} project(s):\n\n"
        for i, project in enumerate(projects[:10], 1):
            title = project.get("title", "Untitled")
            category = project.get("category", "Uncategorized")
            year = project.get("year", "N/A")
            result += f"{i}. **{title}**\n   📂 {category} | 📅 {year}\n\n"
        
        if len(projects) > 10:
            result += f"...and {len(projects) - 10} more projects."
        
        return result
    except Exception as e:
        return f"❌ Error fetching projects: {str(e)}"


@tool
def create_new_project(
    title: str,
    category: str,
    description: str,
    technologies: str,
    year: str = "2024",
    client_name: str = "",
    live_url: str = "",
    github_url: str = ""
) -> str:
    """Create a new portfolio project."""
    try:
        tech_list = [t.strip() for t in technologies.split(",")]
        
        result = api_create_project(
            title=title,
            category=category,
            description=description,
            long_description=description,
            technologies=tech_list,
            year=year,
            client_name=client_name,
            live_url=live_url,
            github_url=github_url
        )
        
        if "error" in str(result).lower():
            return f"❌ Error creating project: {result}"
        
        return f"✅ Project created successfully!\n🗂️ Title: {title}\n📂 Category: {category}"
    
    except Exception as e:
        return f"❌ Error creating project: {str(e)}"


@tool
def list_all_services() -> str:
    """Retrieve and list all available services."""
    try:
        services = api_read_services()
        
        if not services or len(services) == 0:
            return "📭 No services found."
        
        result = f"🛠️ Found {len(services)} service(s):\n\n"
        for i, service in enumerate(services, 1):
            title = service.get("title", "Untitled")
            description = service.get("description", "No description")[:100]
            result += f"{i}. **{title}**\n   {description}...\n\n"
        
        return result
    except Exception as e:
        return f"❌ Error fetching services: {str(e)}"


@tool
def list_contact_inquiries() -> str:
    """Retrieve all contact form inquiries (admin only)."""
    try:
        contacts = api_read_contacts()
        
        if not contacts or len(contacts) == 0:
            return "📭 No contact inquiries found."
        
        result = f"📬 Found {len(contacts)} inquiry/inquiries:\n\n"
        for i, contact in enumerate(contacts[:10], 1):
            name = contact.get("name", "Unknown")
            email = contact.get("email", "N/A")
            message = contact.get("message", "")[:50]
            created = contact.get("created_at", "N/A")[:10] if contact.get("created_at") else "N/A"
            result += f"{i}. **{name}** ({email})\n   📅 {created}\n   💬 {message}...\n\n"
        
        if len(contacts) > 10:
            result += f"...and {len(contacts) - 10} more inquiries."
        
        return result
    except Exception as e:
        return f"❌ Error fetching contacts: {str(e)}"


@tool
def list_all_comments() -> str:
    """Retrieve all blog comments (admin view)."""
    try:
        comments = api_read_comments()
        
        if not comments or len(comments) == 0:
            return "📭 No comments found."
        
        result = f"💬 Found {len(comments)} comment(s):\n\n"
        for i, comment in enumerate(comments[:10], 1):
            author = comment.get("author_name", "Anonymous")
            content = comment.get("content", "")[:80]
            result += f"{i}. **{author}**: {content}...\n\n"
        
        if len(comments) > 10:
            result += f"...and {len(comments) - 10} more comments."
        
        return result
    except Exception as e:
        return f"❌ Error fetching comments: {str(e)}"


@tool
def add_blog_comment(blog_post_id: str, author_name: str, content: str) -> str:
    """Add a comment to a blog post."""
    try:
        result = api_create_comment(
            blog_post_id=blog_post_id,
            author_name=author_name,
            content=content
        )
        
        if "error" in str(result).lower():
            return f"❌ Error adding comment: {result}"
        
        return f"✅ Comment added successfully by {author_name}!"
    
    except Exception as e:
        return f"❌ Error adding comment: {str(e)}"


ALL_TOOLS = [
    generate_content,
    create_blog_post,
    list_all_blogs,
    get_blog_details,
    list_all_projects,
    create_new_project,
    list_all_services,
    list_contact_inquiries,
    list_all_comments,
    add_blog_comment
]
