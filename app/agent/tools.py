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
from blogs.updateBlog import update_blog as api_update_blog
from blogs.deleteBlog import delete_blog as api_delete_blog

from projects.createProject import create_project as api_create_project
from projects.readProject import read_projects as api_read_projects, read_project_by_slug as api_read_project_by_slug
from projects.updateProject import update_project as api_update_project
from projects.deleteProject import delete_project as api_delete_project

from services.readService import read_services as api_read_services, read_service_by_id as api_read_service_by_id
from services.createService import create_service as api_create_service
from services.updateService import update_service as api_update_service
from services.deleteService import delete_service as api_delete_service

from contact.readContact import read_contacts as api_read_contacts
from contact.updateContact import update_contact as api_update_contact
from contact.deleteContact import delete_contact as api_delete_contact

from comments.createComment import create_comment as api_create_comment
from comments.readComment import read_comments as api_read_comments
from comments.deleteComment import delete_comment as api_delete_comment

from testimonials.readTestimonial import read_testimonials as api_read_testimonials
from testimonials.createTestimonial import create_testimonial as api_create_testimonial
from testimonials.updateTestimonial import update_testimonial as api_update_testimonial
from testimonials.deleteTestimonial import delete_testimonial as api_delete_testimonial

from faqs.readFaq import read_faqs as api_read_faqs
from faqs.createFaq import create_faq as api_create_faq
from faqs.updateFaq import update_faq as api_update_faq
from faqs.deleteFaq import delete_faq as api_delete_faq

from stats.readStat import read_stats as api_read_stats
from stats.createStat import create_stat as api_create_stat
from stats.updateStat import update_stat as api_update_stat
from stats.deleteStat import delete_stat as api_delete_stat

from milestones.readMilestone import read_milestones as api_read_milestones
from milestones.createMilestone import create_milestone as api_create_milestone
from milestones.updateMilestone import update_milestone as api_update_milestone
from milestones.deleteMilestone import delete_milestone as api_delete_milestone


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


# ==================== BLOG TOOLS ====================

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
🆔 ID: {blog.get('id', 'N/A')}

📄 Excerpt:
{blog.get('excerpt', 'No excerpt available')}"""
    
    except Exception as e:
        return f"❌ Error fetching blog: {str(e)}"


@tool
def update_blog_post(slug: str, title: str = None, excerpt: str = None, content: str = None, category: str = None, featured: bool = None, published: bool = None) -> str:
    """Update an existing blog post by its slug. Provide only the fields you want to update."""
    try:
        result = api_update_blog(
            slug=slug,
            title=title,
            excerpt=excerpt,
            content=content,
            category=category,
            featured=featured,
            published=published
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating blog: {result}"
        
        return f"✅ Blog updated successfully!\n🔗 Slug: {slug}"
    
    except Exception as e:
        return f"❌ Error updating blog: {str(e)}"


@tool
def delete_blog_post(slug: str) -> str:
    """Delete a blog post by its slug. This action is irreversible."""
    try:
        result = api_delete_blog(slug)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting blog: {result}"
        
        return f"✅ Blog deleted successfully!\n🗑️ Deleted slug: {slug}"
    
    except Exception as e:
        return f"❌ Error deleting blog: {str(e)}"


# ==================== PROJECT TOOLS ====================

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
            slug = project.get("slug", "")
            result += f"{i}. **{title}**\n   📂 {category} | 📅 {year} | 🔗 {slug}\n\n"
        
        if len(projects) > 10:
            result += f"...and {len(projects) - 10} more projects."
        
        return result
    except Exception as e:
        return f"❌ Error fetching projects: {str(e)}"


@tool
def get_project_details(slug: str) -> str:
    """Get details of a specific project by its slug."""
    try:
        project = api_read_project_by_slug(slug)
        
        if not project or "error" in str(project).lower():
            return f"❌ Project not found with slug: {slug}"
        
        technologies = ", ".join(project.get("technologies", [])) or "N/A"
        
        return f"""🗂️ **{project.get('title', 'Untitled')}**

📂 Category: {project.get('category', 'N/A')}
📅 Year: {project.get('year', 'N/A')}
🏢 Client: {project.get('client_name', 'N/A')}
🆔 ID: {project.get('id', 'N/A')}
🔧 Technologies: {technologies}
🌐 Live URL: {project.get('live_url', 'N/A')}
💻 GitHub: {project.get('github_url', 'N/A')}

📄 Description:
{project.get('description', 'No description available')}"""
    
    except Exception as e:
        return f"❌ Error fetching project: {str(e)}"


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
    """Create a new portfolio project. Technologies should be comma-separated."""
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
def update_project(slug: str, title: str = None, category: str = None, description: str = None, technologies: str = None, year: str = None, client_name: str = None, live_url: str = None, github_url: str = None) -> str:
    """Update an existing project by its slug. Provide only the fields you want to update. Technologies should be comma-separated."""
    try:
        tech_list = [t.strip() for t in technologies.split(",")] if technologies else None
        
        result = api_update_project(
            slug=slug,
            title=title,
            category=category,
            description=description,
            long_description=description if description else None,
            technologies=tech_list,
            year=year,
            client_name=client_name,
            live_url=live_url,
            github_url=github_url
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating project: {result}"
        
        return f"✅ Project updated successfully!\n🔗 Slug: {slug}"
    
    except Exception as e:
        return f"❌ Error updating project: {str(e)}"


@tool
def delete_project(slug: str) -> str:
    """Delete a project by its slug. This action is irreversible."""
    try:
        result = api_delete_project(slug)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting project: {result}"
        
        return f"✅ Project deleted successfully!\n🗑️ Deleted slug: {slug}"
    
    except Exception as e:
        return f"❌ Error deleting project: {str(e)}"


# ==================== SERVICE TOOLS ====================

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
            service_id = service.get("id", "N/A")
            result += f"{i}. **{title}** (ID: {service_id})\n   {description}...\n\n"
        
        return result
    except Exception as e:
        return f"❌ Error fetching services: {str(e)}"


@tool
def create_new_service(title: str, description: str, icon: str = "", features: str = "", technologies: str = "") -> str:
    """Create a new service. Features and technologies should be comma-separated."""
    try:
        features_list = [f.strip() for f in features.split(",")] if features else []
        tech_list = [t.strip() for t in technologies.split(",")] if technologies else []
        
        result = api_create_service(
            title=title,
            description=description,
            icon=icon,
            features=features_list,
            technologies=tech_list
        )
        
        if "error" in str(result).lower():
            return f"❌ Error creating service: {result}"
        
        return f"✅ Service created successfully!\n🛠️ Title: {title}"
    
    except Exception as e:
        return f"❌ Error creating service: {str(e)}"


@tool
def update_service(service_id: str, title: str = None, description: str = None, icon: str = None, features: str = None, technologies: str = None) -> str:
    """Update a service by its ID. Provide only the fields you want to update. Features and technologies should be comma-separated."""
    try:
        features_list = [f.strip() for f in features.split(",")] if features else None
        tech_list = [t.strip() for t in technologies.split(",")] if technologies else None
        
        result = api_update_service(
            service_id=service_id,
            title=title,
            description=description,
            icon=icon,
            features=features_list,
            technologies=tech_list
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating service: {result}"
        
        return f"✅ Service updated successfully!\n🆔 ID: {service_id}"
    
    except Exception as e:
        return f"❌ Error updating service: {str(e)}"


@tool
def delete_service(service_id: str) -> str:
    """Delete a service by its ID. This action is irreversible."""
    try:
        result = api_delete_service(service_id)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting service: {result}"
        
        return f"✅ Service deleted successfully!\n🗑️ Deleted ID: {service_id}"
    
    except Exception as e:
        return f"❌ Error deleting service: {str(e)}"


# ==================== CONTACT TOOLS ====================

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
            contact_id = contact.get("id", "N/A")
            created = contact.get("created_at", "N/A")[:10] if contact.get("created_at") else "N/A"
            is_read = "✓" if contact.get("is_read") else "○"
            result += f"{i}. {is_read} **{name}** ({email}) [ID: {contact_id}]\n   📅 {created}\n   💬 {message}...\n\n"
        
        if len(contacts) > 10:
            result += f"...and {len(contacts) - 10} more inquiries."
        
        return result
    except Exception as e:
        return f"❌ Error fetching contacts: {str(e)}"


@tool
def update_contact_inquiry(contact_id: str, is_read: bool = None, status: str = None) -> str:
    """Update a contact inquiry's read status or status by its ID."""
    try:
        result = api_update_contact(
            contact_id=contact_id,
            is_read=is_read,
            status=status
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating contact: {result}"
        
        return f"✅ Contact inquiry updated!\n🆔 ID: {contact_id}"
    
    except Exception as e:
        return f"❌ Error updating contact: {str(e)}"


@tool
def delete_contact_inquiry(contact_id: str) -> str:
    """Delete a contact inquiry by its ID. This action is irreversible."""
    try:
        result = api_delete_contact(contact_id)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting contact: {result}"
        
        return f"✅ Contact inquiry deleted!\n🗑️ Deleted ID: {contact_id}"
    
    except Exception as e:
        return f"❌ Error deleting contact: {str(e)}"


# ==================== COMMENT TOOLS ====================

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
            comment_id = comment.get("id", "N/A")
            result += f"{i}. **{author}** [ID: {comment_id}]: {content}...\n\n"
        
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


@tool
def delete_blog_comment(comment_id: str) -> str:
    """Delete a blog comment by its ID. This action is irreversible."""
    try:
        result = api_delete_comment(comment_id)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting comment: {result}"
        
        return f"✅ Comment deleted successfully!\n🗑️ Deleted ID: {comment_id}"
    
    except Exception as e:
        return f"❌ Error deleting comment: {str(e)}"


# ==================== TESTIMONIAL TOOLS ====================

@tool
def list_all_testimonials(featured_only: bool = False) -> str:
    """Retrieve all testimonials. Set featured_only=True to get only featured ones."""
    try:
        testimonials = api_read_testimonials(featured=featured_only if featured_only else None)
        
        if not testimonials or len(testimonials) == 0:
            return "📭 No testimonials found."
        
        result = f"⭐ Found {len(testimonials)} testimonial(s):\n\n"
        for i, testimonial in enumerate(testimonials[:10], 1):
            author = testimonial.get("author", "Anonymous")
            role = testimonial.get("role", "N/A")
            company = testimonial.get("company", "")
            content = testimonial.get("content", "")[:80]
            testimonial_id = testimonial.get("id", "N/A")
            featured = "⭐" if testimonial.get("featured") else ""
            company_str = f" @ {company}" if company else ""
            result += f"{i}. {featured}**{author}** ({role}{company_str}) [ID: {testimonial_id}]\n   \"{content}...\"\n\n"
        
        if len(testimonials) > 10:
            result += f"...and {len(testimonials) - 10} more testimonials."
        
        return result
    except Exception as e:
        return f"❌ Error fetching testimonials: {str(e)}"


@tool
def create_new_testimonial(author: str, role: str, content: str, company: str = "", rating: int = 5, featured: bool = False) -> str:
    """Create a new testimonial."""
    try:
        result = api_create_testimonial(
            author=author,
            role=role,
            company=company,
            content=content,
            rating=rating,
            featured=featured
        )
        
        if "error" in str(result).lower():
            return f"❌ Error creating testimonial: {result}"
        
        return f"✅ Testimonial created successfully!\n⭐ Author: {author}\n💼 Role: {role}"
    
    except Exception as e:
        return f"❌ Error creating testimonial: {str(e)}"


@tool
def update_testimonial(testimonial_id: str, author: str = None, role: str = None, company: str = None, content: str = None, rating: int = None, featured: bool = None) -> str:
    """Update a testimonial by its ID. Provide only the fields you want to update."""
    try:
        result = api_update_testimonial(
            testimonial_id=testimonial_id,
            author=author,
            role=role,
            company=company,
            content=content,
            rating=rating,
            featured=featured
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating testimonial: {result}"
        
        return f"✅ Testimonial updated successfully!\n🆔 ID: {testimonial_id}"
    
    except Exception as e:
        return f"❌ Error updating testimonial: {str(e)}"


@tool
def delete_testimonial(testimonial_id: str) -> str:
    """Delete a testimonial by its ID. This action is irreversible."""
    try:
        result = api_delete_testimonial(testimonial_id)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting testimonial: {result}"
        
        return f"✅ Testimonial deleted successfully!\n🗑️ Deleted ID: {testimonial_id}"
    
    except Exception as e:
        return f"❌ Error deleting testimonial: {str(e)}"


# ==================== FAQ TOOLS ====================

@tool
def list_all_faqs() -> str:
    """Retrieve all FAQs."""
    try:
        faqs = api_read_faqs()
        
        if not faqs or len(faqs) == 0:
            return "📭 No FAQs found."
        
        result = f"❓ Found {len(faqs)} FAQ(s):\n\n"
        for i, faq in enumerate(faqs[:10], 1):
            question = faq.get("question", "No question")
            answer = faq.get("answer", "")[:80]
            faq_id = faq.get("id", "N/A")
            category = faq.get("category", "General")
            result += f"{i}. **Q:** {question} [ID: {faq_id}]\n   📂 {category}\n   **A:** {answer}...\n\n"
        
        if len(faqs) > 10:
            result += f"...and {len(faqs) - 10} more FAQs."
        
        return result
    except Exception as e:
        return f"❌ Error fetching FAQs: {str(e)}"


@tool
def create_new_faq(question: str, answer: str, category: str = "General") -> str:
    """Create a new FAQ entry."""
    try:
        result = api_create_faq(
            question=question,
            answer=answer,
            category=category
        )
        
        if "error" in str(result).lower():
            return f"❌ Error creating FAQ: {result}"
        
        return f"✅ FAQ created successfully!\n❓ Question: {question[:50]}..."
    
    except Exception as e:
        return f"❌ Error creating FAQ: {str(e)}"


@tool
def update_faq(faq_id: str, question: str = None, answer: str = None, category: str = None) -> str:
    """Update a FAQ by its ID. Provide only the fields you want to update."""
    try:
        result = api_update_faq(
            faq_id=faq_id,
            question=question,
            answer=answer,
            category=category
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating FAQ: {result}"
        
        return f"✅ FAQ updated successfully!\n🆔 ID: {faq_id}"
    
    except Exception as e:
        return f"❌ Error updating FAQ: {str(e)}"


@tool
def delete_faq(faq_id: str) -> str:
    """Delete a FAQ by its ID. This action is irreversible."""
    try:
        result = api_delete_faq(faq_id)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting FAQ: {result}"
        
        return f"✅ FAQ deleted successfully!\n🗑️ Deleted ID: {faq_id}"
    
    except Exception as e:
        return f"❌ Error deleting FAQ: {str(e)}"


# ==================== STAT TOOLS ====================

@tool
def list_all_stats() -> str:
    """Retrieve all stats/metrics displayed on the website."""
    try:
        stats = api_read_stats()
        
        if not stats or len(stats) == 0:
            return "📭 No stats found."
        
        result = f"📊 Found {len(stats)} stat(s):\n\n"
        for i, stat in enumerate(stats, 1):
            label = stat.get("label", "Unknown")
            value = stat.get("value", "N/A")
            icon = stat.get("icon", "")
            stat_id = stat.get("id", "N/A")
            result += f"{i}. {icon} **{label}**: {value} [ID: {stat_id}]\n"
        
        return result
    except Exception as e:
        return f"❌ Error fetching stats: {str(e)}"


@tool
def create_new_stat(label: str, value: str, icon: str = "") -> str:
    """Create a new stat/metric entry."""
    try:
        result = api_create_stat(
            label=label,
            value=value,
            icon=icon
        )
        
        if "error" in str(result).lower():
            return f"❌ Error creating stat: {result}"
        
        return f"✅ Stat created successfully!\n📊 {label}: {value}"
    
    except Exception as e:
        return f"❌ Error creating stat: {str(e)}"


@tool
def update_stat(stat_id: str, label: str = None, value: str = None, icon: str = None) -> str:
    """Update a stat by its ID. Provide only the fields you want to update."""
    try:
        result = api_update_stat(
            stat_id=stat_id,
            label=label,
            value=value,
            icon=icon
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating stat: {result}"
        
        return f"✅ Stat updated successfully!\n🆔 ID: {stat_id}"
    
    except Exception as e:
        return f"❌ Error updating stat: {str(e)}"


@tool
def delete_stat(stat_id: str) -> str:
    """Delete a stat by its ID. This action is irreversible."""
    try:
        result = api_delete_stat(stat_id)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting stat: {result}"
        
        return f"✅ Stat deleted successfully!\n🗑️ Deleted ID: {stat_id}"
    
    except Exception as e:
        return f"❌ Error deleting stat: {str(e)}"


# ==================== MILESTONE TOOLS ====================

@tool
def list_all_milestones() -> str:
    """Retrieve all company milestones/timeline events."""
    try:
        milestones = api_read_milestones()
        
        if not milestones or len(milestones) == 0:
            return "📭 No milestones found."
        
        result = f"🏆 Found {len(milestones)} milestone(s):\n\n"
        for i, milestone in enumerate(milestones, 1):
            year = milestone.get("year", "N/A")
            title = milestone.get("title", "Unknown")
            description = milestone.get("description", "")[:80]
            milestone_id = milestone.get("id", "N/A")
            result += f"{i}. **{year}** - {title} [ID: {milestone_id}]\n   {description}...\n\n"
        
        return result
    except Exception as e:
        return f"❌ Error fetching milestones: {str(e)}"


@tool
def create_new_milestone(year: str, title: str, description: str = "") -> str:
    """Create a new company milestone/timeline event."""
    try:
        result = api_create_milestone(
            year=year,
            title=title,
            description=description
        )
        
        if "error" in str(result).lower():
            return f"❌ Error creating milestone: {result}"
        
        return f"✅ Milestone created successfully!\n🏆 {year} - {title}"
    
    except Exception as e:
        return f"❌ Error creating milestone: {str(e)}"


@tool
def update_milestone(milestone_id: str, year: str = None, title: str = None, description: str = None) -> str:
    """Update a milestone by its ID. Provide only the fields you want to update."""
    try:
        result = api_update_milestone(
            milestone_id=milestone_id,
            year=year,
            title=title,
            description=description
        )
        
        if "error" in str(result).lower():
            return f"❌ Error updating milestone: {result}"
        
        return f"✅ Milestone updated successfully!\n🆔 ID: {milestone_id}"
    
    except Exception as e:
        return f"❌ Error updating milestone: {str(e)}"


@tool
def delete_milestone(milestone_id: str) -> str:
    """Delete a milestone by its ID. This action is irreversible."""
    try:
        result = api_delete_milestone(milestone_id)
        
        if "error" in str(result).lower():
            return f"❌ Error deleting milestone: {result}"
        
        return f"✅ Milestone deleted successfully!\n🗑️ Deleted ID: {milestone_id}"
    
    except Exception as e:
        return f"❌ Error deleting milestone: {str(e)}"


# ==================== ALL TOOLS EXPORT ====================

ALL_TOOLS = [
    generate_content,
    # Blog tools
    create_blog_post,
    list_all_blogs,
    get_blog_details,
    update_blog_post,
    delete_blog_post,
    # Project tools
    list_all_projects,
    get_project_details,
    create_new_project,
    update_project,
    delete_project,
    # Service tools
    list_all_services,
    create_new_service,
    update_service,
    delete_service,
    # Contact tools
    list_contact_inquiries,
    update_contact_inquiry,
    delete_contact_inquiry,
    # Comment tools
    list_all_comments,
    add_blog_comment,
    delete_blog_comment,
    # Testimonial tools
    list_all_testimonials,
    create_new_testimonial,
    update_testimonial,
    delete_testimonial,
    # FAQ tools
    list_all_faqs,
    create_new_faq,
    update_faq,
    delete_faq,
    # Stat tools
    list_all_stats,
    create_new_stat,
    update_stat,
    delete_stat,
    # Milestone tools
    list_all_milestones,
    create_new_milestone,
    update_milestone,
    delete_milestone,
]
