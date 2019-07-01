printf "%-30s %12s %12s\n" "image" "comp_ratio" "png_ratio"

for img in $(find rgb8bit/ -type f | grep .ppm); do
    ppm_bytes=$(du -b "$img" | cut -f 1)

    bname=$(basename "$img")

    outname=output/"${bname%.ppm}".bin
    out_bytes=$(du -b "$outname" | cut -f 1)
    ratio=$(python3 -c "print($ppm_bytes/$out_bytes)")

    outname_png=output/"${bname%.ppm}".png
    out_bytes_png=$(du -b "$outname_png" | cut -f 1)
    ratio_png=$(python3 -c "print(""$ppm_bytes""/""$out_bytes_png"")")

    printf "%-30s %12.6f %12.6f\n" "$bname" "$ratio" "$ratio_png"
done
