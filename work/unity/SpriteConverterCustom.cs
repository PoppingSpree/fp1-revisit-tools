using UnityEditor;
using UnityEngine;
using System.IO;

public class SpriteConverterCustom : EditorWindow
{
    [MenuItem("Tools/FP1 Convert and Set Sprite Properties")]
    static void ConvertAndSetSpriteProperties()
    {
        string folderPath = "Assets/Ann/FP1/FP1Scenes/Resources/Sprites/FP1";
        string[] allFiles = Directory.GetFiles(folderPath, "*.png", SearchOption.AllDirectories);
        int totalFiles = allFiles.Length;
        int processedFiles = 0;

        foreach (string file in allFiles)
        {
            string assetPath = file.Replace(Application.dataPath, "Assets");
            TextureImporter importer = AssetImporter.GetAtPath(assetPath) as TextureImporter;
            
            if (importer != null)
            {
                EditorUtility.DisplayProgressBar("Converting and Setting Sprite Properties", 
                    "Processed "+ processedFiles+" / "+ totalFiles,
                    (float)processedFiles / totalFiles);
                
                importer.textureType = TextureImporterType.Sprite;
                importer.spriteImportMode = SpriteImportMode.Single;
                importer.spritePixelsPerUnit = 1;  // 1 Pixel Per Unit
                importer.filterMode = FilterMode.Point;  // Point Filter
                importer.textureCompression = TextureImporterCompression.Uncompressed;  // No Compression
                
                EditorUtility.SetDirty(importer);
                importer.SaveAndReimport();
                
                processedFiles++;
                if (processedFiles % 10 == 0)  // Update progress every 10 files
                {
                    EditorUtility.DisplayProgressBar("Converting and Setting Sprite Properties", 
                        "Processed "+ processedFiles+" / "+ totalFiles,
                        (float)processedFiles / totalFiles);
                }
            }
        }
        
        EditorUtility.ClearProgressBar();
        AssetDatabase.Refresh();
        Debug.Log("Processed " + processedFiles + " files");
    }
    
    [MenuItem("Tools/FP1 Set Sprite Anchors From Mapping Files")]
    static void SetSpriteAnchorsFromMappingFiles()
    {
        string folderPath = "Assets/Ann/FP1/FP1Scenes/Resources/Sprites/FP1";
        string anchorFolderPath = @"C:\Users\Ann\Downloads\SharedDownloads\code\risingslash-net\fp1-revisit-tools-expanded-suite-auto-dump\fp1-revisit-tools\images\images";
        string[] allFiles = Directory.GetFiles(folderPath, "*.png", SearchOption.AllDirectories);
        int totalFiles = allFiles.Length;
        int processedFiles = 0;

        foreach (string file in allFiles)
        {
            string assetPath = file.Replace(Application.dataPath, "Assets");
            TextureImporter importer = AssetImporter.GetAtPath(assetPath) as TextureImporter;
            
            if (importer != null)
            {
                EditorUtility.DisplayProgressBar("Setting Sprite Anchors", 
                    "Processed "+ processedFiles + " / " + totalFiles,
                    (float)processedFiles / totalFiles);

                // Get the corresponding .anc file path
                string fileName = Path.GetFileNameWithoutExtension(file);
                string ancFilePath = Path.Combine(anchorFolderPath, fileName + ".anc");

                Vector2 pivot = new Vector2(0, 1); // Default to top-left

                if (File.Exists(ancFilePath))
                {
                    string[] anchorData = File.ReadAllText(ancFilePath).Split(',');
                    int x;
                    int y;
                    if (anchorData.Length == 2 && int.TryParse(anchorData[0], out x) && int.TryParse(anchorData[1], out y))
                    {
                        Texture2D texture = AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
                        if (texture != null)
                        {
                            pivot.x = (float)x / texture.width;
                            pivot.y = 1 - (float)y / texture.height; // Invert Y because Unity's Y is bottom-up
                        }
                    }
                }

                importer.spritePivot = pivot;
                // importer.spriteAlignment = (int)SpriteAlignment.Custom;
                
                EditorUtility.SetDirty(importer);
                importer.SaveAndReimport();
                
                processedFiles++;
                if (processedFiles % 10 == 0)
                {
                    EditorUtility.DisplayProgressBar("Setting Sprite Anchors", 
                        "Processed "+ processedFiles + " / " + totalFiles,
                        (float)processedFiles / totalFiles);
                }
            }
        }
        
        EditorUtility.ClearProgressBar();
        AssetDatabase.Refresh();
        Debug.Log("Processed " + processedFiles + " files");
    }
    
    [MenuItem("Tools/FP1 Set All Sprites to Custom Pivot Mode")]
    static void SetAllSpritesToCustomPivotMode()
    {
        string folderPath = "Assets/Ann/FP1/FP1Scenes/Resources/Sprites/FP1";
        string[] allFiles = Directory.GetFiles(folderPath, "*.png", SearchOption.AllDirectories);
        int totalFiles = allFiles.Length;
        int processedFiles = 0;

        foreach (string file in allFiles)
        {
            string assetPath = file.Replace(Application.dataPath, "Assets");
            TextureImporter importer = AssetImporter.GetAtPath(assetPath) as TextureImporter;
        
            if (importer != null)
            {
                EditorUtility.DisplayProgressBar("Setting Custom Pivot Mode", 
                    "Processed " + processedFiles + " / " + totalFiles,
                    (float)processedFiles / totalFiles);

                SpriteMetaData[] spritesheet = importer.spritesheet;
                if (spritesheet != null && spritesheet.Length > 0)
                {
                    for (int i = 0; i < spritesheet.Length; i++)
                    {
                        SpriteMetaData metaData = spritesheet[i];
                        metaData.alignment = (int)SpriteAlignment.Custom;
                        metaData.pivot = importer.spritePivot; // Preserve current pivot
                        spritesheet[i] = metaData;
                    }
                    importer.spritesheet = spritesheet;
                }

                EditorUtility.SetDirty(importer);
                importer.SaveAndReimport();
            
                processedFiles++;
            }
        }
    
        EditorUtility.ClearProgressBar();
        AssetDatabase.Refresh();
        Debug.Log("Set " + processedFiles + " sprites to Custom pivot mode");
    }
}