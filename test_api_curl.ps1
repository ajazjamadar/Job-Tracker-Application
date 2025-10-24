# PowerShell script to test API using Invoke-WebRequest (curl equivalent)

Write-Host "=== Job Application Tracker API Test ===" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://127.0.0.1:5000"

# Create a session to maintain cookies
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$session.UserAgent = "PowerShell API Test"

# Step 1: Login
Write-Host "Step 1: Logging in..." -ForegroundColor Yellow
$loginData = @{
    email = "api_test@example.com"
    password = "password123"
}

try {
    $loginResponse = Invoke-WebRequest -Uri "$baseUrl/auth/login" `
        -Method POST `
        -Body $loginData `
        -WebSession $session `
        -MaximumRedirection 0 `
        -ErrorAction Stop
    
    Write-Host "Success: Login successful (Status: $($loginResponse.StatusCode))" -ForegroundColor Green
}
catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 302) {
        Write-Host "Success: Login successful (redirected)" -ForegroundColor Green
    }
    else {
        Write-Host "Error: Login failed - $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Step 2: GET all applications
Write-Host "Step 2: Getting all applications..." -ForegroundColor Yellow
try {
    $getResponse = Invoke-WebRequest -Uri "$baseUrl/api/applications" `
        -Method GET `
        -WebSession $session
    
    $applications = $getResponse.Content | ConvertFrom-Json
    Write-Host "Success: Retrieved $($applications.Count) application(s)" -ForegroundColor Green
    
    if ($applications.Count -gt 0) {
        Write-Host "  Recent applications:" -ForegroundColor Gray
        $applications | Select-Object -First 3 | ForEach-Object {
            Write-Host "    - $($_.company) - $($_.position) [$($_.status)]" -ForegroundColor Gray
        }
    }
}
catch {
    Write-Host "Error: GET request failed - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Step 3: POST new application (your curl command equivalent)
Write-Host "Step 3: Creating new application (POST)..." -ForegroundColor Yellow
$newApplication = @{
    company = "Acme"
    position = "Engineer"
} | ConvertTo-Json

try {
    $postResponse = Invoke-WebRequest -Uri "$baseUrl/api/applications" `
        -Method POST `
        -Body $newApplication `
        -ContentType "application/json" `
        -WebSession $session
    
    $result = $postResponse.Content | ConvertFrom-Json
    Write-Host "Success: Created application with ID: $($result.id)" -ForegroundColor Green
    Write-Host "  Status Code: $($postResponse.StatusCode)" -ForegroundColor Gray
}
catch {
    Write-Host "Error: POST request failed - $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "  Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# Step 4: Verify the new application was created
Write-Host "Step 4: Verifying new application..." -ForegroundColor Yellow
try {
    $verifyResponse = Invoke-WebRequest -Uri "$baseUrl/api/applications" `
        -Method GET `
        -WebSession $session
    
    $allApplications = $verifyResponse.Content | ConvertFrom-Json
    $acmeApps = $allApplications | Where-Object { $_.company -eq "Acme" }
    
    Write-Host "Success: Found $($acmeApps.Count) application(s) from Acme" -ForegroundColor Green
    $acmeApps | ForEach-Object {
        Write-Host "  - ID: $($_.id) | Company: $($_.company) | Position: $($_.position)" -ForegroundColor Gray
    }
}
catch {
    Write-Host "Error: Verification failed - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Cyan
