def load_css():
    return """
<style>

/* -----------------------------
Overall App
------------------------------*/

.main{
    background-color:#F5F7FB;
}

/* Hide Streamlit Footer */

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* -----------------------------
Main Title
------------------------------*/

.main-title{
    font-size:42px;
    font-weight:700;
    color:#1E3A8A;
    margin-bottom:0px;
}

.subtitle{
    font-size:18px;
    color:#6B7280;
    margin-top:-10px;
    margin-bottom:25px;
}

/* -----------------------------
Dashboard Cards
------------------------------*/

.dashboard-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 4px 18px rgba(0,0,0,0.08);
    text-align:center;
    transition:0.3s;
}

.dashboard-card:hover{

    transform:translateY(-5px);

    box-shadow:0px 8px 24px rgba(0,0,0,0.15);

}

.metric-value{

    font-size:34px;

    font-weight:bold;

    color:#2563EB;

}

.metric-label{

    color:#6B7280;

    font-size:16px;

}

/* -----------------------------
Download Card
------------------------------*/

.download-card{

    background:white;

    padding:20px;

    border-radius:18px;

    box-shadow:0px 4px 18px rgba(0,0,0,0.08);

}

/* -----------------------------
Chat Bubbles
------------------------------*/

.user-bubble{

    background:#DBEAFE;

    padding:15px;

    border-radius:18px;

    margin-top:10px;

    margin-bottom:10px;

}

.ai-bubble{

    background:#F3F4F6;

    padding:15px;

    border-radius:18px;

    margin-bottom:15px;

}

/* -----------------------------
Section Heading
------------------------------*/

.section-title{

    font-size:24px;

    font-weight:bold;

    color:#1F2937;

    margin-bottom:15px;

}

/* -----------------------------
Buttons
------------------------------*/

.stButton>button{

    border-radius:12px;

    height:50px;

    font-size:16px;

    font-weight:bold;

}

</style>
"""