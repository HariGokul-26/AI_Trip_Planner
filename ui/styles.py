import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* ============================================
           Main App
        ============================================ */

        .block-container{
            padding-top:2rem;
            padding-bottom:2rem;
            max-width:1200px;
        }


        /* ============================================
           Hide Streamlit Default Menu & Footer
        ============================================ */

        #MainMenu{
            visibility:hidden;
        }

        footer{
            visibility:hidden;
        }

        /* Keep the sidebar toggle visible. The rest of Streamlit's header
           remains unobtrusive, so the collapsed sidebar always has a way back. */
        header[data-testid="stHeader"]{
            visibility:visible;
            background:transparent;
        }

        header[data-testid="stHeader"] [data-testid="stStatusWidget"]{
            display:none;
        }


        /* ============================================
           Sidebar
        ============================================ */

        section[data-testid="stSidebar"]{
            width:300px;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3{
            color:#1E88E5;
        }


        /* ============================================
           Chat Messages
        ============================================ */

        div[data-testid="stChatMessage"]{
            border-radius:12px;
            padding:10px;
        }


        /* ============================================
           Buttons
        ============================================ */

        .stButton>button{
            width:100%;
            border-radius:10px;
            font-weight:600;
        }

        section[data-testid="stSidebar"] .stButton>button{
            min-height:2rem;
            padding:.35rem .5rem;
            font-size:.86rem;
            text-align:left;
        }


        /* ============================================
           Chat Input
        ============================================ */

        div[data-testid="stChatInput"]{
            padding-top:15px;
        }


        /* ============================================
           Welcome Card
        ============================================ */

        .welcome-card{
            padding:30px;
            border-radius:15px;
            border:1px solid #DDD;
            margin-bottom:25px;
        }


        /* ============================================
           Footer
        ============================================ */

        .footer{
            text-align:center;
            color:gray;
            font-size:14px;
            margin-top:50px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
