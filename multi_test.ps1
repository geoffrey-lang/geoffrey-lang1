# 获取当前时间
$time = Get-Date -Format "MMddHHmm"
$i = 0

# 用户选择城市
$city_choice = Read-Host "请选择城市（1-8）或输入0选择全部"

if (-not $city_choice) {
    Write-Host "未检测到输入，自动选择全部选项..."
    $city_choice = 0
}

# 根据用户选择设置城市和相应的stream
switch ($city_choice) {
    1 { $city = "Shanghai_103"; $stream = "udp/239.45.3.209:5140"; $channel_key = "上海电信" }
    2 { $city = "Beijing_liantong_145"; $stream = "rtp/239.3.1.159:8000"; $channel_key = "北京联通" }
    3 { $city = "Sichuan_333"; $stream = "udp/239.93.1.9:2192"; $channel_key = "四川电信" }
    4 { $city = "Zhejiang_120"; $stream = "rtp/233.50.200.191:5140"; $channel_key = "浙江电信" }
    5 { $city = "Beijing_dianxin_186"; $stream = "udp/225.1.8.37:8002"; $channel_key = "北京电信" }
    6 { $city = "Jieyang_129"; $stream = "hls/38/index.m3u8"; $channel_key = "揭阳" }
    7 { $city = "Guangdong_332"; $stream = "udp/239.77.1.19:5146"; $channel_key = "广东电信" }
    8 { $city = "Henan_327"; $stream = "rtp/239.16.20.1:10010"; $channel_key = "河南电信" }
    0 {
        # 如果选择是“全部选项”，则逐个处理每个选项
        for ($option = 1; $option -le 8; $option++) {
            & .\multi_test.ps1 $option  # 假设脚本名为multi_test.ps1
        }
        exit
    }
    default {
        Write-Host "错误：无效的选择。"
        exit 1
    }
}

# 使用城市名作为默认文件名，格式为 CityName.ip
$filename = "ip\$city.ip"

# 搜索最新ip
Write-Host "===============从tonkiang检索最新ip================="
python hoteliptv.py $channel_key | Out-File -FilePath test.html

# 处理文件
Select-String -Path test.html -Pattern "href='hotellist.html?s=[^']*'" | 
    ForEach-Object { $_.ToString().Split("'")[1].Split("?s=")[1] } | 
    Set-Content -Path $filename

Remove-Item test.html

Write-Host "===============检索完成================="

# 检查文件是否存在
if (-Not (Test-Path $filename)) {
    Write-Host "错误：文件 $filename 不存在。"
    exit 1
}

$lines = (Get-Content $filename).Count
Write-Host "【$filename文件】内ip共计$lines个"

Get-Content $filename | ForEach-Object {
    $i++
    $ip = $_
    $url = "http://$ip/$stream"

    if ($city -eq "Jieyang_129") {
        Write-Host $url
        # 使用 yt-dlp 下载并解析下载速度
        $output = & yt-dlp --ignore-config --no-cache-dir --output "output.ts" --download-archive new-archive.txt --external-downloader ffmpeg --external-downloader-args "-t 5" "$url" 2>&1
        
        # 检查输出并提取下载速度
        if ($output -match 'at ([0-9.]+M)') {
            $a = $matches[1]
        } else {
            $a = ""
        }
        
        Remove-Item new-archive.txt, output.ts
    } else {
        Write-Host $url
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 3 -ErrorAction SilentlyContinue
        $a = if ($response.StatusCode -eq 200) { "Success" } else { "Failed" }
    }

    Write-Host "第$i/$lines个：$ip    $a"
    "$ip    $a" | Out-File -Append -FilePath "speedtest_${city}_$time.log"
}

# 处理结果
Get-Content "speedtest_${city}_$time.log" | Where-Object { $_ -match 'M|k' } | 
    ForEach-Object { $_.Split(" ")[1] + "  " + $_.Split(" ")[0] } | 
    Sort-Object -Descending | Set-Content "result\result_${city}.txt"

Get-Content "result\result_${city}.txt"

# 处理模板
$ip1 = (Get-Content "result\result_${city}.txt")[0].Split(" ")[1]
$ip2 = (Get-Content "result\result_${city}.txt")[1].Split(" ")[1]
$ip3 = (Get-Content "result\result_${city}.txt")[2].Split(" ")[1]

(Get-Content template\template_${city}.txt) -replace "ipipip", $ip1 | Set-Content tmp1.txt
(Get-Content template\template_${city}.txt) -replace "ipipip", $ip2 | Set-Content tmp2.txt
(Get-Content template\template_${city}.txt) -replace "ipipip", $ip3 | Set-Content tmp3.txt
Get-Content tmp1.txt, tmp2.txt, tmp3.txt | Set-Content "txt\$city.txt"

Remove-Item tmp1.txt, tmp2.txt, tmp3.txt

# 生成 zubo.txt
"上海电信,#genre#" | Out-File zubo.txt
Get-Content txt\Shanghai_103.txt | Out-File -Append -FilePath zubo.txt
"北京电信,#genre#" | Out-File -Append -FilePath zubo.txt
Get-Content txt\Beijing_dianxin_186.txt | Out-File -Append -FilePath zubo.txt
"北京联通,#genre#" | Out-File -Append -FilePath zubo.txt
Get-Content txt\Beijing_liantong_145.txt | Out-File -Append -FilePath zubo.txt
"河南电信,#genre#" | Out-File -Append -FilePath zubo.txt
Get-Content txt\Henan_327.txt | Out-File -Append -FilePath zubo.txt
"广东电信,#genre#" | Out-File -Append -FilePath zubo.txt
Get-Content txt\Guangdong_332.txt | Out-File -Append -FilePath zubo.txt
"四川电信,#genre#" | Out-File -Append -FilePath zubo.txt
Get-Content txt\Sichuan_333.txt | Out-File -Append -FilePath zubo.txt
"浙江电信,#genre#" | Out-File -Append -FilePath zubo.txt
Get-Content txt\Zhejiang_120.txt | Out-File -Append -FilePath zubo.txt
"广东揭阳,#genre#" | Out-File -Append -FilePath zubo.txt
Get-Content txt\Jieyang_129.txt | Out-File -Append -FilePath zubo.txt

# 显示结果
Get-ChildItem result\*.txt | ForEach-Object {
    Write-Host ""
    Write-Host "========================= $($_.Name) ==================================="
    Get-Content $_.FullName
}
