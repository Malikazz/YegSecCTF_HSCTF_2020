# Very Safe Login

## The Challenge

We need to log in to a web page. Went to the link in the challenge, attempted to log in with a generic account to see the request. Nothing abnormal. Opted to view the source to see how it works, found that there was javascript for authentication. 

<details><summary>Javascript</summary>
        
        var login = document.login;

        function submit() {
            const username = login.username.value;
            const password = login.password.value;
            
            if(username === "jiminy_cricket" && password === "mushu500") {
                showFlag();
                return false;
            }
            return false;
        }
</details>

Logged in with the username and password that the javascript was looking for and the flag was displayed on the screen.  

## Answer
<details><summary>Spoiler (Output Includes Flag)</summary>
<p>
```
flag{cl13nt_51de_5uck5_135313531}
```

</p>
</details>

---

Danny Klatt
