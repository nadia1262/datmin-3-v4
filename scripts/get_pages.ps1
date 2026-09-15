
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = "D:\POLSTAT STIS\Tingkat 3\Semester 6\DATMIN\Kelompok_3_v4\reports\Laporan_Project_Akhir_Datmin3_FINAL.docx"
$doc = $word.Documents.Open($docPath)
$pages = $doc.ComputeStatistics(2)
Write-Output "PAGE_COUNT: $pages"
$doc.Close(0)
$word.Quit()
