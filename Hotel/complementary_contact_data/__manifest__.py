# -*- coding: utf-8 -*-
{
    "name": "Partners Contact Full Details",
    "version": "12.0.1.0.1",
    "category": "Sales",
    "author": "Odoo Tools",
    "website": "https://odootools.com/apps/12.0/partners-contact-full-details-233",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "web"
    ],
    "data": [
        "data/data.xml",
        "views/extra_contact_info.xml",
        "views/res_partner.xml",
        "security/ir.model.access.csv",
        "views/views.xml"
    ],
    "qweb": [
        "static/src/xml/contact_info_widget.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to keep complete and easy-reach partners' contact information",
    "description": """
    Odoo provides a short list of fields for contact data: phone, mobile, email, and website. Your communication with partners is much more complex. Chat applications nicknames, social media accounts, links to various web pages are extremely valuable for any business today. It is possible to put this information into notes, and... forget that details, since they are out of view and they are ugly ordered. That is why you need this app. It is the tool to have <strong>complete</strong>, <strong>easy-reached</strong>, and <strong>well-structured</strong> contact data for your customers and suppliers.

    The tool is introduced for Odoo partners: suppliers or customers, companies or individuals, contacts, and addresses. Use also <strong>free</strong> add-ons for <a href='https://apps.odoo.com/apps/modules/12.0/complementary_lead_data/'>CRM opportunities</a> and <a href='https://apps.odoo.com/apps/modules/12.0/complementary_employee_data/'>HR Employees</a>
    Contact details are not limited or restricted. Add any sort of partner data and keep as many records you like. Contact information should be full and complete! Have multiple phone and mobile numbers, numerous email addresses, as many Skype or WhatsApps links, etc.
    Each contact detail is easily distinguishable by a clear icon and an optional comment
    A contact record is provided with an own click behaviour to reach the target link or the target application without effort. Have a look at the section <a href='#formats'>supported icons and formats</a>
    ​Drag and drop records to achieve the structure you like
    Copy a contact detail in a single click for immediate using or forwarding
    # <a name='formats'></a>Supported icons and formats
    <p>Contact detail type guarantees a correct behaviour, when you click on a related record. Supported link formats are:</p>
<ul>
<li>
    <i>Phone</i>: to dial a related number. Used for icons:
    <ul>
        <li><i class="fa fa-phone"></i> Phone</li>
        <li><i class="fa fa-volume-control-phone"></i> Mobile</li>
    </ul>
</li>
<li>
    <i>Email</i>: to launch your default email client and to start composing a message for a related address. Used for icons:
    <ul>
        <li><i class="fa fa-envelope-square"></i> Email</li>
    </ul>
</li>
<li>
    <i>Skype</i>: to open the chat with a user related to this phone number in the Skype app. Used for icons:
    <ul>
        <li><i class="fa fa-skype"></i> Skype</li>
    </ul>
</li>
<li>
    <i>WhatsApp</i>: to open the chat with a user related to this phone number in the WhatsApp app. Used for icons:
    <ul>
        <li><i class="fa fa-whatsapp"></i> WhatsApp</li>
    </ul>
</li>
<li>
    <i>Telegram</i>: to open the chat with a user related to this <i>User name</i> in the TG app. Used for icons:
    <ul>
        <li><i class="fa fa-telegram"></i> Telegram</li>
    </ul>
</li>
<li>
    <i>Website url</i>: to open related website pages. Used for icons:
    <ul>
        <li><i class="fa fa-globe"></i> Website</li>
        <li><i class="fa fa-slack"></i> Slack</li>
        <li><i class="fa fa-linkedin"></i> LinkedIn</li>
        <li><i class="fa fa-facebook-official"></i> Facebook</li>
        <li><i class="fa fa-youtube"></i> Twitter</li>
        <li><i class="fa fa-globe"></i> Youtube</li>
        <li><i class="fa fa-google-plus"></i> Google Plus</li>
        <li><i class="fa fa-vk"></i> Vkontakte</li>
        <li><i class="fa fa-instagram"></i> Instagram</li>
        <li><i class="fa fa-pinterest"></i> Pinterest</li>
        <li><i class="fa fa-twitch"></i> Twitch</li>
        <li><i class="fa fa-github"></i> Github</li>
        <li><i class="fa fa-link"></i> Misc Urls - <i>any other</i> website addresses</li>
    </ul>
</li>
<li>
    <i>Miscellaneous</i>: just to show value without any click event. Used for icons:
    <ul>
        <li><i class="fa fa-tag"></i> Misc</li>
    </ul>
</li>
</ul>
    Contact details in readonly mode
    Contact details in readonly mode (more than 7)
    Contact details in readonly mode (expanded)
    Contact details in edit mode
    Well-structured list through drag&drop
    Form to create and edit contact details
    List of available contact info types (icons)
    Empty contact details in edit mode
    Contact info for Odoo partners' contacts (simplified form)
    Contact details for Odoo addresses (simplified form)
    Partners search by contact details
""",
    "images": [
        "static/description/main.png"
    ],
    "price": "28.0",
    "currency": "EUR",
}