from datetime import datetime
import os
from dotenv import load_dotenv


base_url = os.getenv('BASE_URL')

def sign_up(name: str, year=datetime.now().year) -> str:
    body = """
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Onboarding</title>
    <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;700&display=swap"
        rel="stylesheet"> <!-- Google Fonts link -->
    <style>
    body {
    /* font-family: 'Bricolage Grotesque', Arial, sans-serif; */
    font-family: 'Bricolage Grotesque', Arial, sans-serif;

    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

.container {
    max-width: 600px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.headers {
    text-align: left;
    padding: 0px 0px 0px 20px;
    /* background-color: #4CAF50;
    color: #ffffff;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px; */
}

/* .headers h1 {
    /* margin: 0; */
    /* font-size: 9; */
/* } */ 

.content {
    padding: 0px 0px 0px  20px;
}

.logo {
    text-align: left;
}
.logo img {
    max-width: 30%;
    height: auto;
}
.content h2 {
    font-size: 20px;
    
    color: #333333;
}

.content p {
    color: #555555;
    line-height: 1.6;
}

.headers h1 {
    color: #090943;
    
    /* color: red; */
}
.subber {
    color: #F6AD3A
}

.headers h1{
    font-size: 22px;
}

.button {
    display: inline-block;
    padding: 10px 20px;
    margin: 20px 0;
    background-color: #4CAF50;
    color: #ffffff;
    text-decoration: none;
    border-radius: 4px;
}

.footer {
    text-align: center;
    padding: 10px;
    background-color: #f4f4f4;
    color: #777777;
    font-size: 12px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}

@media (max-width: 600px) {
    .container {
        padding: 10px;
    }

    .content h2,
    .content p {
        font-size: 16px;
    }

  

    .button {
        padding: 10px 15px;
    }
}
    </style>
</head>
<body>

    <div class="container">
        <header class="headers">
            <div class="logo">
                <img src="cid:logo" alt="Pathway2Gold Logo">
            
            </div>
            <div></div>
            <h1>Welcome 👋, <span class="subtext" id="subber">""" + name + """</span></h1>
            <!-- <h1>Adeniyi Okunuga</h1> -->
        </header>
        <div class="content">
            <p>
                We're excited to have you join us! Pathway2Gold is here to help you reach yout goals, whether they're
                personal or career-related. We have tools and resources to guide you every steps of the way.
            </p>

            <h2>How to Get Started</h2>
            <p><Strong>Set 4-Digit Passcode:</Strong> To keep your secure, you'll need to st a 4-digit passcode.</p>
            <p><Strong>Verify your Identity:</Strong> You will receive a verification code via email or SMS. Enter this
                code in the app when prompted and also you'll be prompted to verify your identity using NIN and BVN
                verification.</p>
            <p><Strong>Provide some additional details:</Strong> Fill out your profile with some basic details like your
                name, email, address and a bit about youir goals.</p>

            <h3>Need Help?</h3>
            <p>
                Our supporting team is here for you. Visit our Help Center or contact us directly through the app if you
                need assistance. Thank you for choosing Pathway2Gold. We're excited 🎉to help you achieve your goals!
            </p>
        </div>
        <div class="footer">
            &copy; """ + str(year) + """ Pathway2Gold. All rights reserved.
        </div>
    </div>

</body>

</html>
    """
    return body

def otp(code: str, year=datetime.now().year) -> str:
    body = """
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kindly Verify Your Account</title>
    <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;700&display=swap"
        rel="stylesheet"> <!-- Google Fonts link -->
    <style>
        body {
            /* font-family: 'Bricolage Grotesque', Arial, sans-serif; */
            font-family: 'Bricolage Grotesque', Arial, sans-serif;

            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }


        .headers {
            text-align: left;
            padding: 0px 0px 0px 20px;
            /* background-color: #4CAF50;
            color: #ffffff;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px; */
        }


        .code {
            /* background-color:; */
            font-size: 39px;
            font-weight: bold;
            color: #090943;
            margin: 20px 0;
        }
        .headers h1{
            font-size: 22px;
        }


        .content p{
            text-align: left;
        }
        .content {
            padding: 0px 0px 0px  20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            text-align: center;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .logo {
            text-align: left;
        }
        .logo img {
            max-width: 30%;
            height: auto;
        }
    </style>
</head>

<body>

    <div class="container">
        <header class="headers">
            <div class="logo">
                <img src="cid:logo" alt="Pathway2Gold Logo">
            
            </div>
            <div></div>
            <h1>Email Verification</h1>
            <!-- <h1>Adeniyi Okunuga</h1> -->
        </header>
        <div class="content">
            <p>
                This one-time password (OTP) remains active for 30 minutes. Kindly refrain from disclosing this code to anyone.
            </p>
            
        
            <div class="code">""" + code + """</div>
            <p>Please use this code to complete your verification process.</p>
            <p>
                
                If you did not request this code, please ignore this email.</p>
        </div>
        <div class="footer">
            &copy; """ + str(year) + """Pathway2Gold. All rights reserved.
        </div>
    </div>

</body>

</html>
    """
    return body