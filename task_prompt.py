def task_prompt(links):
    return f"""Role: You are acting as a professional software engineer and web designer with expertise in modern UI/UX principles, the React web development frameworks, and mobile-first responsive design. Your task is to redesign the website for a small business using the provided HTML code. Your goal is to improve the website’s user experience, aesthetics, performance, accessibility, and SEO while retaining core business information.
    Instructions:

        Analyze the Current Website:
            I will provide you the HTML source code from the current website and a list of all related URLs (the site’s structure).
            Review the layout, structure, and content of the site. Identify outdated components and areas where the design can be modernized or simplified.
            Assume the current website serves a local business, such as a restaurant or retail shop, where customer engagement and ease of access are critical.

        Redesign Objectives:
            UI/UX: Create a modern, clean, and user-friendly interface. Prioritize mobile responsiveness and ensure that users on mobile, tablet, and desktop devices have a seamless experience.
            Navigation: Improve navigation simplicity while retaining any essential links. Use a minimalistic, intuitive navigation system.
            Visual Appeal: Incorporate a visually attractive, cohesive color scheme, high-quality images, and well-placed call-to-action buttons.
            Speed Optimization: Ensure the design reduces load time by minimizing unnecessary scripts or elements and following best practices like lazy loading and image optimization.
            SEO and Accessibility: Ensure the design is search engine optimized (SEO) with proper meta tags, title hierarchy, and ALT text for images. Follow WCAG accessibility standards for color contrast, ARIA roles, and semantic HTML.

        Required Components:
            Header and Footer: Redesign the header and footer to be consistent, clean, and functional with essential information like contact, social links, and business hours.
            Main Page: Use the homepage to showcase the business’s key offerings, such as a menu for a restaurant or featured products for a retail store.
            Responsive Design: The redesign must support mobile-first principles.
            Forms: Include a contact form, reservation form (for restaurants), or newsletter signup as needed.
            Call-to-Actions: Strategically place CTAs like "Order Now," "Book a Table," or "Contact Us" that are prominent yet not intrusive.

        Design Tools and Technologies:
            You may use the React front-end framework and ensure the code is structured and scalable. Recommend the best front-end stack for this business.
            The CSS should be modern, with a preference for CSS Grid, Flexbox, or any CSS-in-JS solutions for styling.
            Suggest any modern tools or libraries you deem necessary to improve functionality (e.g., animations, carousel, or image galleries).

        Structure of Website: Here’s the structure of the website for reference (list of base URLs):

        {links}

        Deliverables:
            Provide the fully redesigned HTML code with CSS and JavaScript recommendations.
            Include explanations for key design decisions and any external libraries or frameworks you suggest integrating.
            If possible, provide a list of improvements you made in terms of performance, UI/UX, and SEO.
            The code should be fully functional and ready for deployment to a live server."""